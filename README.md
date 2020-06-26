# edge_dec

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


# https://github.com/pgmadonia/codeastro_project
# https://docs.google.com/document/d/1LHPVT1-NCDTH9OjoixNIdyduie8LyfZIZuvtWFv5yg0/edit

