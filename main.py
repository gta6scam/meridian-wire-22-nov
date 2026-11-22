#!/usr/bin/env python3
"""Hand-in program for THE MERIDIAN WIRE (news-image-20261122).

The front page is composed by draw.py and committed as entry.png;
this program only delivers it: it copies entry.png into the output
directory named by the MAKEFUN_OUTPUT_DIR environment variable
(falling back to /output). No network, no clocks, deterministic.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    print("delivered:", dest)


if __name__ == "__main__":
    main()
