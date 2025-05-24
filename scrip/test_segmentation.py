import unittest
import numpy as np
import rasterio # Ensure rasterio is imported if open_img will be used directly or for context

# Assuming 'open_img' is in 'files.py' and 'classify' is in 'segmentrgb.py'
# Adjust the import paths if your file structure is different or if they are part of a package
from .files import open_img
from .segmentrgb import classify

class TestSegmentation(unittest.TestCase):

    def setUp(self):
        # Define the path to the test image.
        # Assuming the test is run from the root directory or a location where 'example/sugarcane.tif' is accessible.
        # If tests are run from the 'scrip' directory, the path might need adjustment (e.g., '../example/sugarcane.tif')
        self.test_image_path = "../example/sugarcane.tif" # Adjusted path
        self.input_image, self.profile = open_img(self.test_image_path)
        # It's good practice to ensure the image was loaded
        if self.input_image is None:
            raise FileNotFoundError(f"Test image not found at {self.test_image_path}")


    def test_classify_output_properties(self):
        """Test basic properties of the output mask from the classify function."""
        # Process the image using the classify function
        # Ensure win_size is appropriate for the test image; it might need adjustment
        # or to be determined from image properties if necessary.
        mask = classify(self.input_image, win_size=50)

        # 1. Check if the output mask is a numpy array
        self.assertIsInstance(mask, np.ndarray, "Mask is not a numpy array.")

        # 2. Check if the output mask is binary (contains only 0s and 1s)
        # This assumes that the mask uses 0 and 1. If it uses boolean True/False,
        # you might convert it or check for boolean type.
        # Using np.unique to find all unique values in the mask.
        # Depending on the process, it might also contain NaN or other values if errors occur or no plants are found.
        # For a simple binary mask, we expect values like [0, 1] or just [0] or just [1].
        unique_values = np.unique(mask)
        is_binary = np.all(np.isin(unique_values, [0, 1]))
        self.assertTrue(is_binary, f"Mask is not binary. Unique values found: {unique_values}")

        # 3. Check if the output mask has compatible dimensions
        # The classify function in segmentrgb.py transposes the mask dimensions at the end.
        # Original image shape (height, width, channels) from open_img (after transpose): (width, height, channels)
        # So, input_image.shape[0] is width, input_image.shape[1] is height.
        # The mask is (original_ty, original_tx), which corresponds to (input_image.shape[1], input_image.shape[0])
        expected_height = self.input_image.shape[1] # Original ty
        expected_width = self.input_image.shape[0]  # Original tx
        
        self.assertEqual(mask.shape[0], expected_height, "Mask height does not match expected height.")
        self.assertEqual(mask.shape[1], expected_width, "Mask width does not match expected width.")

    def test_classify_handles_small_image(self):
        """Test how classify handles an image smaller than win_size."""
        # Create a small dummy image (e.g., 30x30 pixels)
        small_image_data = np.random.randint(0, 256, size=(30, 30, 3), dtype=np.uint8)
        
        # Since classify directly uses the image data, we can pass it.
        # Ensure win_size is larger than the image dimensions.
        mask = classify(small_image_data, win_size=50)

        self.assertIsInstance(mask, np.ndarray, "Mask is not a numpy array for small image.")
        
        # Check dimensions (should match the small image)
        self.assertEqual(mask.shape[0], small_image_data.shape[1]) # Transposed logic
        self.assertEqual(mask.shape[1], small_image_data.shape[0])

        # Check if binary (even if it's all 0s or all 1s)
        unique_values = np.unique(mask)
        is_binary = np.all(np.isin(unique_values, [0, 1]))
        self.assertTrue(is_binary, f"Mask is not binary for small image. Unique values: {unique_values}")


if __name__ == '__main__':
    unittest.main()
