# -*- coding: utf-8 -*-
"""
Scrip to read a raster file (RGB image) and save a bimary image (mask).
Open a file with the field boundary and crop the raster (RGB image).

@author: Leonardo Felipe Maldaner
"""
import geopandas as gpd
import json
import rasterio
from rasterio.mask import mask

def check_scr(img, bound):
    srci = img.crs
    if img.crs is None:
        img.crs = 'epsg:4323'
    srcb = bound.crs
    return srci

def getFeatures(gdf):
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def cropimg(file, mtx):
    """Crop raster
    """
    shp = gpd.read_file(file)
    geoms = getFeatures(shp)
    out_mtx, out_transform = mask(dataset=mtx,shapes=geoms, crop=True)
    return out_mtx, out_transform

def open_img(pathimg, pathbou=None):
    """Open Geotiff image and boundary shapefile

    Parameters
    ----------
    pathimg : str
        Raster Geotiff path.
    pathbou : str
        path of the shapefile (.shp).

    Returns
    -------
    rgb : array (int)
        array 3D with RGB colors
    out_meta : dict
        distionary with Geotiff metadata

    """
    with rasterio.open(pathimg) as mtx:

        if pathbou is not None:
            out_mtx, out_transform = cropimg(pathbou, mtx)
        else:
            out_mtx = mtx.read()
            out_transform = mtx.transform

        out_meta = mtx.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_mtx.shape[1],
                         "width": out_mtx.shape[2],
                         "transform": out_transform,
                         "dtype": rasterio.uint8,
                         "count": 1,
                         "compress": "lzw"})

        out_mtx = out_mtx.transpose()
        out_mtx = out_mtx[:, :, 0:3]

    return out_mtx, out_meta

def save_img(mtx, pfile, pathout):
    """Save mask as raster Geotiff.
    """
    with rasterio.open(pathout, 'w', **pfile) as dst:
        dst.write(mtx.astype(rasterio.uint8), 1)
