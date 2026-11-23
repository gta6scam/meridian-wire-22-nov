#!/usr/bin/env python3
"""Hand-in for The Meridian Wire, day-2 challenger (News Image 20261122).

The front page is drawn locally by the build pipeline and committed as
entry.png next to this file. The hand-in's only job is to place that exact
file where the grader expects it: the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default /output). Nothing is
rendered at hand-in time, so the graded bytes are the committed bytes.

Revision: after copying, the hand-in verifies its own work. The final
phase re-runs this program in a sandbox where a short or corrupted write
would otherwise be graded silently as a broken page; instead, the copy
is read back and compared with the bundled entry.png by size and
SHA-256, and any mismatch exits non-zero with the reason on stderr, so
a damaged hand-in fails loudly rather than scoring as a damaged page.
Standard library only.
"""
import hashlib
import os
import shutil
import sys


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src) or _sha256(dst) != _sha256(src):
        print("entry.png copy failed integrity check (size/sha256 mismatch)",
              file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
