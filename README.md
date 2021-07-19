# Find plants in RGB image

Scrip para identificar plantas de cana-de-açúcar em imagens RGB geradas por RPA's

Classificação não-supervisionada com o algoritmo k-means

Os pacotes necessários são:

```
fiona
rasterio
skimage
sklearn.cluster
numpy
collections
```

Para processar as imagens basta usar o arquivo teste.py

```python
from files import open_img, save_mask
from segmentrgb import classify

pathimg = r'example\sugarcane.tif'
pathout = r'example\mask.tif'

#open image
image, profile = open_img(pathimg)

#process image
mask = classify(image, win_size=50)

#save mask
save_mask(mask, profile, pathout)
```
