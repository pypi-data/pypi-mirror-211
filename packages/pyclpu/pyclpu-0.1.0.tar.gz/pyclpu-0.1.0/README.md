**This file describes the module of CLPU utilities and related aspects to users and maintainers.**

# CLPU Utilities

**Abstract:** This module bundels functions which are frequently used for applications at the Centro de Laseres Pulsados, Villamayor, Spain. Although we intend to deliver reliable software solutions, we can not guarantee that every implementation is flawless. We encourage the user to re-read the code and alert us if bugs are found.

## Scripts

### Image Module

#### Warp Transform

The class allows to transform a linearly distorted input image into a trapez-corrected view on it. The class can be used in a functional way

```
from pyclpu import image

warp = image.PerspectiveTransform(source = image.imread("path/to/test.jpg")) 
```

with the warped image in `warp.warped` and the coordinates of cornes from the source image stored in `sourcecorners`. Note that the source image is not part of the object in its final form. A more object oriented use case can deal with loops where all warps have the same source corner coordinates

```
from pyclpu import image

warp_it = image.PerspectiveTransform()

image_stack = image.imread(path/to/directory/with/many/images/)

warp = []

for image in image_stack:
    warp_it.source = image
    warp.append[{"warped" : warp.warped, "sourcecorners" : warp.sourcecorners}]
```

with results beeing stored in a list `warp`.

## Installation

Run `pip install pyclpu` when connected to the internet or `pip install .` within the main folder of the project if not connected to the internet.

## Developper's Guide

Create the anaconda environment in Anaconda based on the `clpu.yml` file delivered in the main folder of the project, e.g. in the Anaconda prompt with `conda env create -f path/to/clpu.yml` and activate it with `conda activate clpu`.

### Export

Before exporting a new version of the module

- increase the version counters in `setup.py` and `pyclpu\__init__.py`,
- update the `.yml`file if needed via `conda env export > clpu.yml`,
- commit the code into the developper's branch `dev` with a note on the new version number,
- merge the developper's branch into the main branch `master`.

Export with `python setup.py sdist` to `dist/`. Then to upload all distributions created under `dist/` execute `twine upload dist/*`or to upload the source distribution with a gpg signature `twine upload dist/pyexample-0.1.0.tar.gz pyexample-0.1.0.tar.gz.asc`. Now the distribution is updated in pyPIP. For the Anaconda version, run 

