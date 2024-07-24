import os


def get_path_to(directory: str) -> str:
    """Get the absolute path to a directory."""
    return os.path.abspath(os.path.join(os.getcwd(), directory))


# Available directories
ICON_DIRECTORY = "../assets/icons"
CMAPS_DIRECTORY = "../assets/cmaps"

# Paths to directories
PATH_TO_ICON_DIRECTORY = get_path_to(ICON_DIRECTORY)
PATH_TO_CMAPS_DIRECTORY = get_path_to(CMAPS_DIRECTORY)
