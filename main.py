#!/usr/bin/env python3
"""Hand-in for The Meridian Wire (News Image 20261122, @yutulboy).

Copies the committed entry.png into MAKEFUN_OUTPUT_DIR.
The artwork itself is built locally by draw.py; this file only
performs the copy, using nothing but the standard library.
"""
import os
import shutil


def main():
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
