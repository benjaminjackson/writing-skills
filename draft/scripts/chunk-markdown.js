#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const file = process.argv[2];

if (!file) {
  console.error("Usage: chunk-markdown.js <file.md>");
  process.exit(2);
}

if (!fs.existsSync(file)) {
  console.error(`Missing file: ${file}`);
  process.exit(1);
}

const source = fs.readFileSync(file, "utf8");
let tokenCounter;

function tksCount(text) {
  if (tokenCounter === "estimate") return null;
  const result = spawnSync("tks", { input: text, encoding: "utf8" });
  if (result.status !== 0) {
    tokenCounter = "estimate";
    return null;
  }
  tokenCounter = "tks";
  const match = result.stdout.match(/\d+/);
  return match ? Number(match[0]) : null;
}

function estimateTokens(text) {
  const exact = tksCount(text);
  if (exact !== null) return exact;
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  return Math.ceil(words * 1.3);
}

function withoutFrontmatter(text) {
  if (!text.startsWith("---\n")) return { text, offset: 0, frontmatter: false };
  const end = text.indexOf("\n---", 4);
  if (end === -1) return { text, offset: 0, frontmatter: false };
  const after = text.indexOf("\n", end + 4);
  const start = after === -1 ? text.length : after + 1;
  return { text: text.slice(start), offset: text.slice(0, start).split(/\n/).length - 1, frontmatter: true };
}

function isSkippable(block) {
  return block
    .split(/\n/)
    .every((line) => {
      const trimmed = line.trim();
      return (
        trimmed === "" ||
        /^[-*]\s+\[[ xX]\]\s*[_\s:.-]*$/.test(trimmed) ||
        /^[-*]\s*[_\s:.-]+$/.test(trimmed)
      );
    });
}

function blocksFromMarkdown(text, lineOffset) {
  const lines = text.split(/\n/);
  const blocks = [];
  let current = [];
  let startLine = lineOffset + 1;
  let heading = "document";

  function flush(endLine) {
    const raw = current.join("\n").trim();
    if (raw && !isSkippable(raw)) {
      blocks.push({ text: raw, startLine, endLine, heading });
    }
    current = [];
  }

  lines.forEach((line, index) => {
    const lineNo = lineOffset + index + 1;
    const headingMatch = line.match(/^(#{1,6})\s+(.+?)\s*$/);

    if (line.trim() === "") {
      flush(lineNo - 1);
      startLine = lineNo + 1;
      return;
    }

    if (current.length === 0) startLine = lineNo;
    current.push(line);

    if (headingMatch) heading = headingMatch[2];
  });

  flush(lineOffset + lines.length);
  return blocks;
}

function splitLongBlock(block, maxTokens) {
  if (estimateTokens(block.text) <= maxTokens * 2) return [block];

  const parts = block.text
    .split(/(?<=\.)\s+|(?<=\?)\s+|(?<=!)\s+|\n(?=\s*[-*]\s+)/)
    .map((part) => part.trim())
    .filter(Boolean);

  const chunks = [];
  let current = [];

  for (const part of parts) {
    const candidate = [...current, part].join(" ");
    if (current.length && estimateTokens(candidate) > maxTokens) {
      chunks.push({ ...block, text: current.join(" "), partial: true });
      current = [part];
    } else {
      current.push(part);
    }
  }

  if (current.length) chunks.push({ ...block, text: current.join(" "), partial: true });
  return chunks;
}

function passOneChunks(blocks) {
  const expanded = blocks.flatMap((block) => splitLongBlock(block, 400));
  const chunks = [];
  let current = [];

  function emit() {
    if (!current.length) return;
    const text = current.map((block) => block.text).join("\n\n");
    chunks.push({
      id: `p1-${chunks.length + 1}`,
      pass: 1,
      location: current[0].heading,
      start_line: current[0].startLine,
      end_line: current[current.length - 1].endLine,
      token_count: estimateTokens(text),
      partial: current.some((block) => block.partial),
      text,
    });
    current = [];
  }

  for (const block of expanded) {
    const blockTokens = estimateTokens(block.text);
    if (blockTokens > 400) {
      emit();
      chunks.push({
        id: `p1-${chunks.length + 1}`,
        pass: 1,
        location: block.heading,
        start_line: block.startLine,
        end_line: block.endLine,
        token_count: blockTokens,
        partial: Boolean(block.partial),
        text: block.text,
      });
      continue;
    }

    const candidate = [...current, block].map((item) => item.text).join("\n\n");
    if (current.length && estimateTokens(candidate) > 400) emit();
    current.push(block);
  }

  emit();
  return chunks;
}

function sectionsForPassTwo(blocks) {
  const totalText = blocks.map((block) => block.text).join("\n\n");
  if (estimateTokens(totalText) <= 4000) {
    return [{
      id: "p2-1",
      pass: 2,
      location: "whole document",
      start_line: blocks[0]?.startLine || 1,
      end_line: blocks[blocks.length - 1]?.endLine || 1,
      token_count: estimateTokens(totalText),
      text: totalText,
    }];
  }

  const sections = [];
  let current = [];
  for (const block of blocks) {
    const isTopHeading = /^##\s+/.test(block.text);
    if (isTopHeading && current.length) {
      sections.push(current);
      current = [];
    }
    current.push(block);
  }
  if (current.length) sections.push(current);

  return sections.map((section, index) => {
    const text = section.map((block) => block.text).join("\n\n");
    return {
      id: `p2-${index + 1}`,
      pass: 2,
      location: section[0].heading,
      start_line: section[0].startLine,
      end_line: section[section.length - 1].endLine,
      token_count: estimateTokens(text),
      oversize: estimateTokens(text) > 3000,
      text,
    };
  });
}

const stripped = withoutFrontmatter(source);
const blocks = blocksFromMarkdown(stripped.text, stripped.offset);
const pass1 = passOneChunks(blocks);
const pass2 = sectionsForPassTwo(blocks);

console.log(JSON.stringify({
  file: path.normalize(file),
  frontmatter_skipped: stripped.frontmatter,
  token_counter: tokenCounter || "estimate",
  pass1,
  pass2,
}, null, 2));
