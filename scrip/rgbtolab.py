# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:38:09 2021

@author: Leonardo Felipe Maldaner (leonardofm@usp.br)
"""

from skimage.color import rgb2lab

def calclab(img):
    """
    RGB to l*a*b*
    """
    lab = rgb2lab(img) 
    ab = lab[:, :, 1:3]
    return ab

