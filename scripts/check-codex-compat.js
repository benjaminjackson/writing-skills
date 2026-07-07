#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = process.cwd();
const errors = [];
const warnings = [];

function relPath(...parts) {
  return path.join(root, ...parts);
}

function exists(rel) {
  return fs.existsSync(relPath(rel));
}

function read(rel) {
  return fs.readFileSync(relPath(rel), "utf8");
}

function addError(message) {
  errors.push(message);
}

function addWarning(message) {
  warnings.push(message);
}

function parseJson(rel) {
  try {
    return JSON.parse(read(rel));
  } catch (error) {
    addError(`${rel}: invalid JSON: ${error.message}`);
    return null;
  }
}

function ensureFile(rel) {
  if (!exists(rel)) addError(`${rel}: missing file`);
}

function ensureDir(rel) {
  const full = relPath(rel);
  if (!fs.existsSync(full) || !fs.statSync(full).isDirectory()) {
    addError(`${rel}: missing directory`);
  }
}

function walk(dir, predicate = () => true) {
  const fullDir = relPath(dir);
  if (!fs.existsSync(fullDir)) return [];

  const out = [];
  for (const entry of fs.readdirSync(fullDir, { withFileTypes: true })) {
    if (entry.name === ".git") continue;
    const rel = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...walk(rel, predicate));
    } else if (predicate(rel)) {
      out.push(rel);
    }
  }
  return out;
}

function validatePlugin(rel, expectedName) {
  const manifestPath = path.join(rel, ".codex-plugin", "plugin.json");
  ensureFile(manifestPath);
  const manifest = parseJson(manifestPath);
  if (!manifest) return;

  if (manifest.name !== expectedName) {
    addError(`${manifestPath}: expected name ${expectedName}, got ${manifest.name}`);
  }

  if (!manifest.version || !/^\d+\.\d+\.\d+$/.test(manifest.version)) {
    addError(`${manifestPath}: version must be strict semver`);
  }

  if (!manifest.description) addError(`${manifestPath}: missing description`);
  if (!manifest.author || !manifest.author.name) addError(`${manifestPath}: missing author.name`);
  if (!manifest.skills) addError(`${manifestPath}: missing skills path`);

  if (manifest.skills) {
    const skillsPath = path.join(rel, manifest.skills.replace(/^\.\//, ""));
    ensureDir(skillsPath);
  }

  if (!manifest.interface || !manifest.interface.displayName) {
    addError(`${manifestPath}: missing interface.displayName`);
  }
}

function validateMarketplace() {
  const rel = ".agents/plugins/marketplace.json";
  ensureFile(rel);
  const marketplace = parseJson(rel);
  if (!marketplace) return;

  if (!marketplace.name) addError(`${rel}: missing name`);
  if (!Array.isArray(marketplace.plugins)) addError(`${rel}: plugins must be an array`);

  for (const plugin of marketplace.plugins || []) {
    const name = plugin.name || "(missing name)";
    if (!plugin.name) addError(`${rel}: plugin entry missing name`);
    if (!plugin.source || plugin.source.source !== "local") {
      addError(`${rel}: ${name} must use local source`);
      continue;
    }
    if (!plugin.source.path || !plugin.source.path.startsWith("./")) {
      addError(`${rel}: ${name} source.path must start with ./`);
      continue;
    }

    const pluginDir = plugin.source.path.replace(/^\.\//, "");
    ensureDir(pluginDir);
    ensureFile(path.join(pluginDir, ".codex-plugin", "plugin.json"));

    if (!plugin.policy || !plugin.policy.installation || !plugin.policy.authentication) {
      addError(`${rel}: ${name} missing policy.installation or policy.authentication`);
    }
    if (!plugin.category) addError(`${rel}: ${name} missing category`);
  }
}

function validateSkillFrontmatter() {
  const skillFiles = walk(".", (rel) => rel.endsWith("SKILL.md"));
  for (const rel of skillFiles) {
    const body = read(rel);
    const match = body.match(/^---\n([\s\S]*?)\n---/);
    if (!match) {
      addError(`${rel}: missing YAML frontmatter`);
      continue;
    }
    const frontmatter = match[1];
    if (!/^name:\s*\S/m.test(frontmatter)) addError(`${rel}: frontmatter missing name`);
    if (!/^description:\s*\S/m.test(frontmatter)) addError(`${rel}: frontmatter missing description`);
  }
}

function validateOpenAiYaml() {
  const files = walk(".", (rel) => rel.endsWith(path.join("agents", "openai.yaml")));
  for (const rel of files) {
    const body = read(rel);
    for (const key of ["interface:", "display_name:", "short_description:", "default_prompt:"]) {
      if (!body.includes(key)) addError(`${rel}: missing ${key}`);
    }
    const policyMatch = body.match(/allow_implicit_invocation:\s*(\S+)/);
    if (policyMatch && !["true", "false"].includes(policyMatch[1])) {
      addError(`${rel}: allow_implicit_invocation must be true or false`);
    }
  }
}

function validateDocsInstallCoverage() {
  const docs = ["README.md", "docs/codex-compatibility-plan.md", "docs/agent-portability.md"]
    .filter(exists)
    .map(read)
    .join("\n");

  if (!docs.includes("/plugin marketplace add")) {
    addError("docs: missing Claude install command coverage");
  }
  if (!docs.includes("codex plugin marketplace add")) {
    addError("docs: missing Codex install command coverage");
  }
  if (!read("README.md").includes("codex plugin marketplace add")) {
    addWarning("README.md: Codex install docs are still pending");
  }
}

function reportClaudeOnlyTerms() {
  const terms = [
    { name: "Agent(", pattern: /Agent\s*\(/ },
    { name: "SendMessage", pattern: /SendMessage/ },
    { name: "AskUserQuestion", pattern: /AskUserQuestion/ },
    { name: "WebSearch", pattern: /WebSearch/ },
    { name: "WebFetch", pattern: /WebFetch/ },
    { name: "subagent_type", pattern: /subagent_type/ },
  ];
  const files = [
    ...walk("draft/skills", (rel) => rel.endsWith(".md")),
    ...walk("draft/references", (rel) => rel.endsWith(".md")),
    ...walk("pitch/skills", (rel) => rel.endsWith(".md")),
    ...walk("pitch/references", (rel) => rel.endsWith(".md")),
  ];

  for (const rel of files) {
    const lines = read(rel).split(/\r?\n/);
    lines.forEach((line, index) => {
      for (const term of terms) {
        if (term.pattern.test(line)) {
          addWarning(`${rel}:${index + 1}: inspect transitional Claude-only term ${term.name}`);
        }
      }
    });
  }
}

for (const rel of [
  ".claude-plugin/marketplace.json",
  "draft/.claude-plugin/plugin.json",
  "pitch/.claude-plugin/plugin.json",
  "draft/.codex-plugin/plugin.json",
  "pitch/.codex-plugin/plugin.json",
]) {
  ensureFile(rel);
  parseJson(rel);
}

validateMarketplace();
validatePlugin("draft", "draft");
validatePlugin("pitch", "pitch");
validateSkillFrontmatter();
validateOpenAiYaml();
validateDocsInstallCoverage();
reportClaudeOnlyTerms();

if (warnings.length) {
  console.log("Compatibility warnings:");
  for (const warning of warnings) console.log(`- ${warning}`);
  console.log("");
}

if (errors.length) {
  console.error("Compatibility check failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log("Compatibility check passed.");
