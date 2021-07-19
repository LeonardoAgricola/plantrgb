# -*- coding: utf-8 -*-
"""
Split the RGB image into small windows and performs the unsupervised 
classification of each window.

@author: Leonardo Felipe Maldaner
"""

import numpy as np

from mask import labels2mask
from clusterkmeans import cal_cluster
from rgbtolab import calclab


def classify(rgb, win_size=50):
    """

    Parameters
    ----------
    rgb : 3D arrray (int)

    win_size : int
        Size of the window to split the image into smaller parts.
        The default is 50.

    Returns
    -------
    mask : boolean


    """
    resx = rgb.shape[0]//(round(rgb.shape[0]/win_size))
    resy = rgb.shape[1]//(round(rgb.shape[1]/win_size))
    tx = rgb.shape[0]
    ty = rgb.shape[1]

    window = [rgb[x:x+resx, y:y+resy, :] for x in range(0, tx, resx) for y in range(0, ty, resy)]
    sxy = [(x.shape[0], x.shape[1]) for x in window]

    lab = [calclab(x) for x in window]

    labels = [cal_cluster(x) for x in lab]

    labelsxy = list(zip(labels, sxy))
    masks = [labels2mask(x, y) for x, y in labelsxy]

    mask = np.zeros([ty, tx])
    count = 0
    for locx in range(0, tx, resx):
        for locy in range(0, ty, resy):
            mask[locy:locy+resy, locx:locx+resx] = masks[count].T
            count = count + 1
    return mask
