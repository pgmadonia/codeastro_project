# edgedec
## a package to find edges between colors in a picture

This package uses matplotlib.image to load a picture into memory as a Picture object.

The series of commands to transform a picture into contours:

pip install edgedec

ipython

import edgedec

image = edgedec.Picture('file_name.png')

image.paint_contours()

~ OR ~

image.paint_contours(grad = True) # to paint only strong edges

~ OR ~

image.paint_contours(grad = True, threshold = 0.1) # from 0.01 to 1

 [![Documentation Status](https://readthedocs.org/projects/docs/badge/?version=latest)](https://edgedec.readthedocs.io/en/latest/index.html) [![PyPI version](https://badge.fury.io/py/edgedec.svg)](https://badge.fury.io/py/edgedec)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
