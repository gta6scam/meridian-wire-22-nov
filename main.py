#!/usr/bin/env python3
"""Hand-in for The Meridian Wire (round 4, @yutulboy).

Copy pattern: the finished page is committed as entry.png beside
this file; at grading time we simply copy it to the location the
runner names in MAKEFUN_OUTPUT_DIR.  Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
