#!/usr/bin/env python3
"""Hand-in for The Meridian Wire, round 3 (News Image 20261122).

The page itself is rendered locally by draw.py and committed as
entry.png; this hand-in only copies that file into the directory the
grader points at through MAKEFUN_OUTPUT_DIR (falling back to /output).
Standard library only.
"""
import os
import shutil


def deliver():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(target_dir, "entry.png"))


if __name__ == "__main__":
    deliver()
