#!/usr/bin/env python3
"""Report content in OUTPUT that does not appear in INPUT.

Usage: python3 draft/evals/invented.py INPUT OUTPUT

Checks three kinds of content an editor must never add: numbers, quotations
and proper nouns. Prints one `kind: item` line per new item and exits 1 when
it finds any. Prints nothing and exits 0 when the output adds none.

Stdlib only, so it runs without the PyYAML the eval runner needs.
"""
import re
import sys
from pathlib import Path

NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
    "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
    "eighteen": "18", "nineteen": "19", "twenty": "20",
    "hundred": "100", "thousand": "1000", "million": "1000000",
    "percent": "%", "half": "half", "dozen": "12", "twice": "twice",
}

# Day and month names are capitalised by rule, not because they are names, so
# a new one is never reported as an invented proper noun.
CALENDAR_WORDS = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
}

# Characters that close a sentence or a clause, so the next word may be
# capitalised for grammar rather than because it is a name.
SENTENCE_END = (".", "!", "?", ":")

# Curly quotation marks, written as escapes so they are easy to tell apart.
LEFT_DOUBLE = "“"
RIGHT_DOUBLE = "”"
LEFT_SINGLE = "‘"
RIGHT_SINGLE = "’"


def strip_front_matter(text):
    """Drop a leading YAML block between two `---` lines, if there is one."""
    if not text.startswith("---\n"):
        return text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return text
    return parts[2]


def numbers(text):
    """Return the numbers in the text, normalised so "2" and "two" match."""
    found = []
    # "40 percent" and "40%" are the same number; fold the word form first.
    text = re.sub(r"(\d)\s*percent\b", r"\1%", text, flags=re.I)
    # A digit run, with optional thousands commas or a decimal part, and an
    # optional percent sign.
    for match in re.finditer(r"\d+(?:[.,]\d+)*%?", text):
        found.append(match.group(0).replace(",", ""))
    for word in re.findall(r"[A-Za-z]+", text):
        lowered = word.lower()
        if lowered in NUMBER_WORDS:
            found.append(NUMBER_WORDS[lowered])
    return found


def normalise_quote(text):
    """Lower-case, fold curly quotes and collapse whitespace, for comparison."""
    text = text.replace(LEFT_SINGLE, "'").replace(RIGHT_SINGLE, "'")
    text = text.replace(LEFT_DOUBLE, '"').replace(RIGHT_DOUBLE, '"')
    text = re.sub(r"\s+", " ", text.lower())
    return text.strip(" .,;:!?'\"")


def quotations(text):
    """Return every span inside double or single quotes, straight or curly.

    A single quote only opens a quotation when no letter comes right before
    it, and only closes one when no letter comes right after it, so the
    apostrophes in "don't" and "Ana's" are not read as quotation marks.
    """
    patterns = [
        r'"([^"\n]+)"',
        LEFT_DOUBLE + "([^" + RIGHT_DOUBLE + r"\n]+)" + RIGHT_DOUBLE,
        r"(?<![A-Za-z])'([^'\n]+?)'(?![A-Za-z])",
        "(?<![A-Za-z])" + LEFT_SINGLE + "([^" + RIGHT_SINGLE + r"\n]+?)" + RIGHT_SINGLE + "(?![A-Za-z])",
    ]
    spans = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            spans.append(match.group(1))
    return spans


def capitalised_mid_sentence(text):
    """Return capitalised words that are not first in a sentence or line.

    A word right after a colon, a list marker or a heading marker counts as
    first. "I" and its contractions never count. A possessive ending is
    dropped, and a hyphenated name such as "Priya-Jones" stays one word.
    """
    quote_marks = "\"'" + LEFT_DOUBLE + RIGHT_DOUBLE + LEFT_SINGLE + RIGHT_SINGLE
    words_found = []
    for line in text.splitlines():
        # Drop heading hashes, list markers ("-", "*", "1.") and blockquotes.
        line = re.sub(r"^\s*(#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s*)+", "", line)
        previous = None
        for raw in line.split():
            # Strip quotes, brackets and markdown emphasis around the word.
            word = raw.strip(quote_marks + "()[]*_`")
            is_first = previous is None or previous.rstrip(quote_marks + ")*_").endswith(SENTENCE_END)
            previous = raw
            if is_first or not word or not word[0].isupper():
                continue
            # Drop a possessive ending: "Ana's" is Ana, "Jones'" is Jones.
            base = re.split("['" + RIGHT_SINGLE + "]", word)[0]
            base = base.rstrip(".,;:!?")
            if base == "I":
                continue
            parts = base.split("-")
            if not all(part.isalpha() for part in parts):
                continue
            words_found.append(base)
    return words_found


def known_word(word, source_words):
    """True when a capitalised word is a day, a month, or already in the source.

    A plural of a source word counts as known ("Sundays" when the source says
    "Sunday"). A hyphenated word is known only when every part is.
    """
    for part in word.lower().split("-"):
        forms = [part]
        if part.endswith("s"):
            forms.append(part[:-1])
        if part.endswith("es"):
            forms.append(part[:-2])
        known = False
        for form in forms:
            if form in source_words or form in CALENDAR_WORDS:
                known = True
        if not known:
            return False
    return True


def main():
    """Compare OUTPUT against INPUT and print every item OUTPUT added."""
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    source = strip_front_matter(Path(sys.argv[1]).read_text())
    output = strip_front_matter(Path(sys.argv[2]).read_text())

    hits = []
    source_numbers = set(numbers(source))
    for number in numbers(output):
        if number not in source_numbers:
            hits.append(f"number: {number}")

    # A quotation in the output must come from a quotation in the source.
    # Words the source says in its own voice, put in quote marks, are invented.
    source_quotes = [normalise_quote(span) for span in quotations(source)]
    for span in quotations(output):
        quoted = normalise_quote(span)
        if not any(quoted in source_quote for source_quote in source_quotes):
            hits.append(f"quotation: {span}")

    source_words = set(word.lower() for word in re.findall(r"[A-Za-z]+", source))
    for word in capitalised_mid_sentence(output):
        if not known_word(word, source_words):
            hits.append(f"proper noun: {word}")

    # dict.fromkeys keeps the first occurrence of each line, in order.
    for line in dict.fromkeys(hits):
        print(line)
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
