import numpy as np
from utils.constants import FILE_METADATA_DICT_KEYS, IMAGE_METADATA_DICT_KEYS, STANDARDISED_METADATA_DICT_KEYS


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
            self.contained_in_folder = None

            self.initialized = True  # Ensure init is called only once

    def load_new_file_data(self, filepath: str, file_ext: str, frames: np.ndarray | list | tuple, 
                           file_metadata: list, channels: list, contained_in_folder: bool = False):
        """Load new file data into the manager, resetting previous data."""
        # Reset all variables
        self.reset()

        # Convert frames to np.array if not already
        if isinstance(frames, (list, tuple)):
            frames = np.array(frames, dtype=np.float16)
        
        if frames.ndim not in [2, 3]:
            raise ValueError("Frames must be a 2D or 3D array.")
        
        # Add a new axis to handle images as if they are frames
        if frames.ndim == 2:
            frames = np.expand_dims(frames, axis=0)

        if len(file_metadata) != len(STANDARDISED_METADATA_DICT_KEYS):
            raise ValueError("The length of file_metadata does not match the required metadata keys.")  

        # Store file metadata
        file_metadata_values = [
            file_metadata["Frames"],
            file_metadata["Speed (FPS)"],
            file_metadata["Line/s (Hz)"],
            file_metadata["Y Pixel Dimensions"],
            file_metadata["X Pixel Dimensions"],
            file_metadata["Current channel"],
            channels
        ]    


        frame_metadata_dictionary = {}

        # Store frames metdata
        # Lookup method: frame_metadata_dictonary[frame_no]["name of variable"]
        for frame_no in range(file_metadata["Frames"]):
            frame_metadata_values = [
                file_metadata["X Range (nm)"],
                file_metadata["Pixel/nm Scaling Factor"],
                np.max(frames[frame_no]),
                np.min(frames[frame_no])
            ]
            frame_metadata_dictionary[frame_no] = dict(zip(IMAGE_METADATA_DICT_KEYS, frame_metadata_values))


        # Store the rest of the variables to the class
        self.filepath = filepath
        self.file_ext = file_ext
        self.file_metadata = dict(zip(FILE_METADATA_DICT_KEYS, file_metadata_values))
        self.image_data = frames
        self.image_metadata = frame_metadata_dictionary
        self.contained_in_folder = contained_in_folder

        self.output_file_data()


    def get_channels(self) -> list:
        return self.file_metadata["Available Channels"]

    def output_file_data(self, show_image_data: bool = False):
        print(f"File path: {self.filepath}")
        print(f"File ext: {self.file_ext}")
        print(f"File metadata: {self.file_metadata}")
        if show_image_data == True:
            print(f"File image data: {self.image_data}") 
        print(f"File image metadata: {self.image_metadata}")
        print(f"Is in folder?: {self.contained_in_folder}")

    def reset(self):
        """Reset all stored data to None."""
        self.filepath = None
        self.file_ext = None
        self.file_metadata = None
        self.image_data = None
        self.image_metadata = None
        self.channels = None
        self.contained_in_folder = None
