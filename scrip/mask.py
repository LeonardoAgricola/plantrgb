# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:12:09 2021

@author: Leonardo Felipe Maldaner
"""
from collections import Counter
import numpy as np
from skimage import morphology

def filters(cls, plant):
    """
    Morphological filters
    """

    if np.isnan(cls).all():
        clean = np.zeros(cls.shape)
    else:
        clean = cls == plant
        selem = morphology.disk(2)
        clean = morphology.remove_small_objects(clean, 15)
        clean = morphology.dilation(clean, selem)
        clean = morphology.remove_small_holes(clean, 15)
    return clean


def labels2mask(labels, shp):
    """
    Convert labels in a binary mask with 0 and 1 values
    """
    sizex, sizey = shp
    img = labels[:, 1]
    cls = labels[:, 0]
    maska = np.zeros((sizex, sizey))
    maska[:, :] = np.nan
    if np.all(cls == 10):
        return maska
    else:
        clust = cls[cls != 10]
        tab = Counter(clust)
        tab = sorted(tab, key=tab.get)
        estat = {}
        for i in range(0, len(tab)):
            filtro = cls == i
            value = np.mean(img[filtro])
            estat.update({i:value})
        estat = sorted(estat, key=estat.get)
        plant = estat[0]
        clst = cls.reshape((sizex, sizey))
        maska = filters(clst, plant)
        return maska
    