# -*- coding: utf-8 -*-
"""
Process UAV image Geotiff to sugarcane plant detection
"""

from files import open_img, save_mask
from segmentrgb import classify

pathimg = r'example\sugarcane.tif'
pathout = r'example\maks.tif'

#open image
image, profile = open_img(pathimg)

#process image
mask = classify(image, win_size=50)

#save mask
save_mask(mask, profile, pathout)
