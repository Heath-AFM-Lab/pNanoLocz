import numpy as np
from utils.constants import FILE_METADATA_DICT_KEYS, IMAGE_METADATA_DICT_KEYS


class MediaDataManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MediaDataManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.filepath = None
            self.file_ext = None
            self.file_metadata = None
            self.image_data = None
            self.image_metadata = None
            self.channels = None
            self.contained_in_folder = None

            self.initialized = True  # Ensure init is called only once

    def load_new_file_data(self, filepath: str, file_ext: str, frames: np.ndarray | list | tuple, 
                           file_metadata: list, channels: list, contained_in_folder: bool):
        """Load new file data into the manager, resetting previous data."""
        # Reset all variables
        self.reset()

        # Convert frames to np.array if not already
        if isinstance(frames, (list, tuple)):
            frames = np.array(frames, dtype=np.float16)
        elif not isinstance(frames, np.ndarray):
            raise ValueError("Frames must be a list, tuple, or numpy array of floats.")
        
        if frames.ndim not in [2, 3]:
            raise ValueError("Frames must be a 2D or 3D array.")

        self.image_data = frames

        # Check if file_metadata has the correct size
        if not isinstance(file_metadata, list):
            raise ValueError("Metadata must be provided as a list.")
        
        if len(file_metadata) != len(FILE_METADATA_DICT_KEYS):
            raise ValueError("The length of file_metadata does not match the required metadata keys.")

        # Create the metadata dictionary
        self.file_metadata = dict(zip(FILE_METADATA_DICT_KEYS, file_metadata))

        # Store the rest of the variables to the class
        self.filepath = filepath
        self.file_ext = file_ext
        self.image_metadata = None  # TODO: implement image metadata
        self.channels = channels
        self.contained_in_folder = contained_in_folder

    def reset(self):
        """Reset all stored data to None."""
        self.filepath = None
        self.file_ext = None
        self.file_metadata = None
        self.image_data = None
        self.image_metadata = None
        self.channels = None
        self.contained_in_folder = None
