# edge_dec

edgedec - a package to find edges between colors in a picture

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
