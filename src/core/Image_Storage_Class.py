import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from utils.constants import FILE_METADATA_DICT_KEYS, IMAGE_METADATA_DICT_KEYS, STANDARDISED_METADATA_DICT_KEYS

class MediaDataManager(QObject):
    _instance = None
    
    new_file_loaded = pyqtSignal()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MediaDataManager, cls).__new__(cls)
            # Initialize QObject here
            QObject.__init__(cls._instance)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.file_path = None
        self.file_ext = None
        self.file_metadata = None
        self.image_data = None
        self.image_metadata = None
        self.channels = None
        self.contained_in_folder = None
        self._initialized = True

    def __init__(self):
        # This method is now empty to avoid re-initialization
        pass

    def load_new_file_data(self, file_path: str, file_ext: str, frames: np.ndarray | list | tuple, 
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
        print(frames.ndim, frames.shape, len(frames), file_metadata["Frames"])

        # Store frames metadata
        for frame_no in range(file_metadata["Frames"]):
            frame_metadata_values = [
                file_metadata["X Range (nm)"],
                file_metadata["Pixel/nm Scaling Factor"],
                np.max(frames[frame_no]),
                np.min(frames[frame_no])
            ]
            frame_metadata_dictionary[frame_no] = dict(zip(IMAGE_METADATA_DICT_KEYS, frame_metadata_values))

        # Store the rest of the variables to the class
        self.file_path = file_path
        self.file_ext = file_ext
        self.file_metadata = dict(zip(FILE_METADATA_DICT_KEYS, file_metadata_values))
        self.image_data = frames
        self.image_metadata = frame_metadata_dictionary
        self.contained_in_folder = contained_in_folder

        self.new_file_loaded.emit()
        self.output_file_data()

    # Getter functions, direct from dict
    def get_file_path(self) -> str:
        return self.file_path
    
    def get_frames_amount(self) -> int:
        return self.file_metadata["Frames"]
    
    def get_initial_x_range(self) -> float:
        return self.image_metadata[0]["X Range (nm)"]
    
    def get_fps_speed(self) -> float:
        return self.file_metadata["Speed (FPS)"]
    
    def get_line_frequency(self) -> float:
        return self.file_metadata["Line/s (Hz)"]
    
    def get_y_dims(self) -> int:
        return self.file_metadata["Y Pixel Dimensions"]
    
    def get_x_dims(self) -> int:
        return self.file_metadata["X Pixel Dimensions"]
    
    def get_initial_pix_nm_scaling(self) -> float:
        return self.image_metadata[0]["Pixel/nm Scaling Factor"]
    
    def get_cw_channel(self) -> str:
        return self.file_metadata["Current channel"]     

    def get_channels_list(self) -> list:
        return self.file_metadata["Available channels"]
    
    # Getter functions. Retrieves lists and dicts
    def get_file_metadata(self) -> dict:
        return self.file_metadata
    
    def get_frames_metadata_per_frame(self, frame_no: int) -> dict:
        return self.image_metadata[frame_no]
    
    def get_frames_metadata(self) -> dict:
        return self.image_metadata
    
    def get_frames(self) -> np.ndarray:
        return self.image_data
    

    
    
    
    
    # Debugger function
    def output_file_data(self, show_image_data: bool = False):
        print(f"File path: {self.file_path}")
        print(f"File ext: {self.file_ext}")
        print(f"File metadata: {self.file_metadata}")
        if show_image_data:
            print(f"File image data: {self.image_data}") 
        print(f"Is in folder?: {self.contained_in_folder}")

    def reset(self):
        """Reset all stored data to None."""
        self.file_path = None
        self.file_ext = None
        self.file_metadata = None
        self.image_data = None
        self.image_metadata = None
        self.channels = None
        self.contained_in_folder = None
