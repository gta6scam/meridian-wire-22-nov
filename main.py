#!/usr/bin/env python3
"""Hand-in for The Meridian Wire, day-2 challenger (News Image 20261122).

The front page is drawn locally by the build pipeline and committed as
entry.png next to this file. The hand-in's only job is to place that exact
file where the grader expects it: the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default /output). Nothing is
rendered at hand-in time, so the graded bytes are the committed bytes.
Standard library only.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
