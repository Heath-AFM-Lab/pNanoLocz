import os
import numpy as np
import matplotlib.colors as mcolors
from vispy.color import Colormap
from utils.constants import PATH_TO_CMAPS_DIRECTORY

def load_npy_array(filename: str) -> np.ndarray:
    """Load a NumPy array from a .npy file.

    Args:
        filename (str): Path to the .npy file.

    Returns:
        np.ndarray: The NumPy array loaded from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file does not contain a valid NumPy array.
    """
    file_location = os.path.join(PATH_TO_CMAPS_DIRECTORY, filename)

    if not os.path.exists(file_location):
        raise FileNotFoundError(f"The file '{filename}' does not exist.")

    try:
        data = np.load(file_location)
        return data
    except Exception as e:
        raise ValueError(f"An error occurred while loading the file: {e}")


def create_colormap(cmap_array: np.ndarray):
    """Create Matplotlib colormaps from a NumPy array.

    Args:
        cmap_array (np.ndarray): The NumPy array defining the colormap.

    Returns:
        tuple: A tuple containing Matplotlib and Vispy colormaps.
    """
    # Create Matplotlib colormap
    mpl_cmap = mcolors.ListedColormap(cmap_array)
    
    return mpl_cmap


# Define and load colormap arrays
# TODO: add any more cmaps as needed
CMAPS = {}

cmap_names = ["AFM Brown", "AFM Dark Gold", "AFM Fire", "AFM Gold", "AFM Orange", "Rainbow"]
DEFAULT_CMAP_NAME = cmap_names[0]
for name in cmap_names:
    cmap_array = load_npy_array(f"{name.replace(' ', '_')}.npy")
    mpl_cmap = create_colormap(cmap_array)
    CMAPS[name] = mpl_cmap

# Example usage:
# Access Matplotlib colormap: CMAPS["AFM Brown"]

