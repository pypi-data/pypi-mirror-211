**This file describes the module of CLPU utilities and related aspects to users and maintainers.**

# CLPU Utilities

**Abstract:** This module bundels functions which are frequently used for applications at the Centro de Laseres Pulsados, Villamayor, Spain. Although we intend to deliver reliable software solutions, we can not guarantee that every implementation is flawless. We encourage the user to re-read the code and alert us if bugs are found.

## Scripts

## Installation

## Export

Before exporting a new version of the module

- increase the version counters in `setup.py` and `pyclpu\__init__.py`,
- commit the code into the developper's branch `dev` with a note on the new version number,
- merge the developper's branch into the main branch `master`.

Export with `python setup.py sdist` to `dist/`. Then to upload all distributions created under `dist/` execute `twine upload dist/*`or to upload the source distribution with a gpg signature `twine upload dist/pyexample-0.1.0.tar.gz pyexample-0.1.0.tar.gz.asc`.

