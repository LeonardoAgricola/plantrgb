# -*- coding: utf-8 -*-
"""
Unsupervised classification using k-means algorithm.

@author: Leonardo Felipe Maldaner
"""
import numpy as np
from sklearn.cluster import KMeans

def cal_cluster(win_ab, n_class):
    """Get the classes from the unsupervised classification

    Parameters
    ----------
    win_ab : array (float)
        One-color component a* with shape NxM
		
	n_class : number of cluster (int)

    Returns
    -------
    labels : array (int)
        KMeans labels output with shape N*M

    """
    model = KMeans(n_clusters=n_class,
                   max_iter=3,
                   random_state=43,
                   algorithm='elkan')

    win_ab = win_ab[:, :, 0]

    sizex, sizey = win_ab.shape
    new_ab = win_ab.reshape(sizex*sizey, 1)

    index = new_ab[:, 0] != 0
    new_a = new_ab[index, :]

    labels = np.zeros((sizex*sizey, 2))
    labels[:, 0] = 10
    labels[:, 1] = new_ab[:, 0]

    if new_a.shape[0] > n_class:
        classes = model.fit(new_a)
        labels[index, 0] = classes.labels_

    return labels
