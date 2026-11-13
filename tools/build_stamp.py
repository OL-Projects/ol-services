#!/usr/bin/env python3
"""Build the two facts this site must never have typed by hand.

1. The sample PDF's byte size and sha256, written into the sample card.
2. A build stamp for the footer: sha256 over every published text file, with the
   stamp itself normalised out, so the number is reproducible and changes when
   any published byte changes.

Idempotent: running it twice produces the same files.

    python3 tools/build_stamp.py           # write
    python3 tools/build_stamp.py --check   # exit 1 if a file is out of date
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "sample-estimate.pdf")

TEXT_EXT = {".html", ".css", ".json", ".txt", ".xml", ".svg"}
STAMP_RE = re.compile(r'(<span id="build">)([0-9a-f]{12}|BUILDSTAMP)(</span>)')
SKIP_DIRS = {".git", "tools", "node_modules"}


def published_files():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            ext = os.path.splitext(name)[1].lower()
            if ext in TEXT_EXT:
                out.append(os.path.join(base, name))
    return out


def normalise(text):
    """The stamp value must not feed its own hash."""
    return STAMP_RE.sub(r"\1BUILDSTAMP\3", text)


def build_stamp(read):
    h = hashlib.sha256()
    for path in published_files():
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(read(path).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:12]


def main():
    check = "--check" in sys.argv
    pdf_bytes = open(PDF, "rb").read()
    subs = {
        "{{SAMPLE_SIZE_FR}}": f"{len(pdf_bytes):,}".replace(",", " ") + " octets",
        "{{SAMPLE_SIZE_EN}}": f"{len(pdf_bytes):,} bytes",
        "{{SAMPLE_SHA}}": hashlib.sha256(pdf_bytes).hexdigest(),
    }

    cache = {}

    def read(path):
        if path not in cache:
            with open(path, encoding="utf-8") as fh:
                cache[path] = fh.read()
        return cache[path]

    # The sample card's size and hash are baked into the page (GitHub Pages
    # serves the committed file, there is no render step at deploy), so the
    # replacement has to recognise an already-baked value as well as the token —
    # otherwise a rebuilt PDF leaves a stale size and hash on the page.
    meta_re = re.compile(
        r"(PDF · sample-estimate\.pdf · )([^·<]*?)( · sha256 )([0-9a-f]{64}|\{\{SAMPLE_SHA\}\})")

    def render(path, rel):
        text = read(path)
        for token, value in subs.items():
            text = text.replace(token, value)
        size = subs["{{SAMPLE_SIZE_EN}}"] if rel.startswith("en/") else subs["{{SAMPLE_SIZE_FR}}"]
        sha = subs["{{SAMPLE_SHA}}"]
        return meta_re.sub(lambda m: m.group(1) + size + m.group(3) + sha, text)

    stamp = build_stamp(lambda p: normalise(render(p, os.path.relpath(p, ROOT).replace(os.sep, "/"))))
    print(f"sample: {len(pdf_bytes)} bytes  sha256 {subs['{{SAMPLE_SHA}}']}")
    print(f"build stamp: {stamp}")

    stale = []
    for path in published_files():
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        text = render(path, rel)
        new = STAMP_RE.sub(lambda m: m.group(1) + stamp + m.group(3), text)
        if new != text:
            stale.append(rel)
        if not check and new != text:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)

    if stale:
        print(("stale: " if check else "updated: ") + ", ".join(stale))
        if check:
            return 1
    else:
        print("all files current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
