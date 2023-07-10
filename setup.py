# -*- coding: utf-8 -*-

import re
from setuptools import setup, Extension

PACKAGE = "cohort_parallel"

# extract the version from file version.txt
with open("version.txt") as f:
    VERSION = f.read().strip()

# generate __init__.py from __init__.py.in
init_file = ""
with open(f"{PACKAGE}/__init__.py.in") as fi:
    init_file = re.sub(r"@VERSION@", VERSION, fi.read())
    with open(f"{PACKAGE}/__init__.py", "w") as fo:
        fo.write(init_file)

setup(
)
