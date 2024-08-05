import os

# NanoLocz File and Image Extensions
FILE_EXTS = ['.asd', '.ibw', '.spm', '.jpk', '.gwy', '.ARIS', '.nhf']
IMG_EXTS = ['.nhf', '.jpk', '.ibw', '.spm', '.gwy']


def get_path_to(directory: str) -> str:
    """Get the absolute path to a directory."""
    return os.path.abspath(os.path.join(os.getcwd(), directory))


# Available directories
ICON_DIRECTORY = "../assets/icons"
CMAPS_DIRECTORY = "../assets/cmaps"

# Paths to directories
PATH_TO_ICON_DIRECTORY = get_path_to(ICON_DIRECTORY)
PATH_TO_CMAPS_DIRECTORY = get_path_to(CMAPS_DIRECTORY)

FILE_METADATA_DICT_KEYS = [
    "Frames", "Speed (FPS)", "Line/s (Hz)", "Y Pixel Dimensions", 
    "X Pixel Dimensions", "Current channel", "Available channels"
]

IMAGE_METADATA_DICT_KEYS = [
    "X Range (nm)", "Pixel/nm Scaling Factor", "Max pixel value", "Min pixel value"
]

# TODO: This needs to be edited later to include additional metadata that is not ready yet
STANDARDISED_METADATA_DICT_KEYS = [
    "Frames", "X Range (nm)", "Speed (FPS)", "Line/s (Hz)", "Y Pixel Dimensions", 
    "X Pixel Dimensions", "Pixel/nm Scaling Factor", "Current channel"
]

NANOMETRES_IN_METRE = 1e9
