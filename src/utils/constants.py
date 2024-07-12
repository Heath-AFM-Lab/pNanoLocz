import os
from utils.Folder_Opener_Module.folderOpener import FolderOpener
 
# Icon directory relative to current working directory (/src/)
ICON_DIRECTORY = "../assets/icons"
# Path to icon directory
PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
