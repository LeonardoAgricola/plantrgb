# Plant Identification in RGB Imagery

This project provides scripts to identify plants in high-resolution RGB (Red, Green, Blue) imagery using an unsupervised k-means clustering algorithm. The primary goal is to generate a binary mask that isolates individual plants within agricultural fields.

## Project Structure

The project is organized into the following main components:

- `example/`: Contains an example GeoTIFF image (`sugarcane.tif`) for testing the scripts.
- `scrip/`: Contains all the Python scripts for the image processing pipeline.

## Scripts Description

The `scrip/` directory includes:

-   **`clusterkmeans.py`**: Implements the k-means clustering algorithm. It takes image data (specifically the 'a*' component from LAB color space) and groups pixels into a specified number of classes.
-   **`files.py`**: Contains utility functions for handling file operations. This includes:
    -   Opening GeoTIFF images.
    -   Optionally cropping images based on a provided shapefile boundary.
    -   Saving the processed binary mask as a GeoTIFF file.
-   **`mask.py`**: Responsible for creating the final binary mask. It applies morphological operations (like dilation and removal of small objects/holes) to the classified image to refine the plant segmentation.
-   **`rgbtolab.py`**: Handles the color space conversion from RGB to CIELAB (LAB). The LAB color space is often used in image processing as it separates color information from lightness, which can be beneficial for clustering.
-   **`segmentrgb.py`**: This is the main script that orchestrates the entire segmentation process. It:
    -   Divides the input RGB image into smaller windows (tiles).
    -   Processes each window by converting it to LAB, then applying k-means clustering.
    -   Generates a binary mask for each window using the `mask.py` script.
    -   Stitches the masks from all windows back together to form the final mask for the entire image.
-   **`run_example.py`**: An example script demonstrating how to use the image processing pipeline. It opens an image, processes it using `segmentrgb.classify()`, and saves the resulting mask.

## Getting Started

### Prerequisites

Make sure you have Python installed. The scripts rely on the following Python libraries:

-   `numpy`
-   `scikit-learn`
-   `scikit-image` (for `skimage`)
-   `rasterio`
-   `geopandas`

You can install these dependencies using pip:

```bash
pip install numpy scikit-learn scikit-image rasterio geopandas
```

### Running the Example

1.  Navigate to the project's root directory.
2.  The `scrip/run_example.py` script provides a straightforward way to process an image.
    ```bash
    python scrip/run_example.py
    ```
3.  This script will:
    -   Open the `example/sugarcane.tif` image.
    -   Process it to identify plants.
    -   Save the resulting binary mask to `example/maks.tif`.

### Input

-   **RGB Image**: The primary input is a GeoTIFF (`.tif`) image in the RGB color space. An example is provided in `example/sugarcane.tif`.
-   **Boundary Shapefile (Optional)**: The `files.py` script can optionally take a shapefile (`.shp`) to crop the input image to a specific area of interest before processing.

### Output

-   **Binary Mask**: The script generates a binary GeoTIFF image where plant pixels are typically represented by one value (e.g., 1 or True) and background pixels by another (e.g., 0 or False). The default output for the example is `example/maks.tif`.
