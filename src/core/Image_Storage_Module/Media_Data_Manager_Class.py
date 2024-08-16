import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from utils.constants import FILE_METADATA_DICT_KEYS, IMAGE_METADATA_DICT_KEYS, STANDARDISED_METADATA_DICT_KEYS
from .Media_Storage_Class import MediaStorage

class MediaDataManager(QObject):
    _instance = None
    
    new_file_loaded = pyqtSignal()
    current_mode_changed = pyqtSignal(str)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MediaDataManager, cls).__new__(cls)
            QObject.__init__(cls._instance)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.storage = {
            'Target': MediaStorage(),
            'Preview': MediaStorage(),
            'Original': MediaStorage()
        }
        self.current_mode = 'Target'
        self._initialized = True

    def __init__(self):
        pass

    def set_mode(self, mode: str):
        if mode not in self.storage:
            raise ValueError(f"Invalid mode. Must be one of: {', '.join(self.storage.keys())}")
        self.current_mode = mode
        self.current_mode_changed.emit(mode)

    def get_mode(self) -> str:
        return self.current_mode
    
    def get_mode_list(self) -> list:
        return self.storage.keys()

    def load_new_file_data(self, file_path: str, file_ext: str, frames: np.ndarray | list | tuple, 
                           file_metadata: list, channels: list):
        self.storage[self.current_mode].load_new_file_data(file_path, file_ext, frames, file_metadata, channels)

        # Propagate a copy of the storage across the entire dict
        self.copy_storage_across_dict(from_type=self.current_mode)

        self.set_mode("Original")
        self.new_file_loaded.emit()

    def load_new_folder_data(self, folder_path: str, dominant_file_ext: str, frames: np.ndarray | list | tuple, 
                             folder_metadata: list, channels: list):
        self.storage[self.current_mode].load_new_folder_data(folder_path, dominant_file_ext, frames, folder_metadata, channels)

        # Propagate a copy of the storage across the entire dict
        self.copy_storage_across_dict(from_type=self.current_mode)

        self.set_mode("Original")
        self.new_file_loaded.emit()

    
    def compare_storages(self, storage_type1: str, storage_type2: str) -> bool:
        """
        Compare two storage instances.
        """
        if storage_type1 not in self.storage or storage_type2 not in self.storage:
            raise ValueError("Invalid storage type")
        return self.storage[storage_type1] == self.storage[storage_type2]

    def copy_storage(self, from_type: str, to_type: str):
        """
        Copy one storage instance to another.
        """
        if from_type not in self.storage:
            raise ValueError(f"Invalid 'from' storage type: {from_type}")
        self.storage[to_type] = self.storage[from_type].copy()

    def copy_storage_across_dict(self, from_type):
        """
        Copy one storage across the Media data manager
        """
        for name in self.storage.keys():
            if name != from_type:
                self.copy_storage(from_type=from_type, to_type=name)

    
    # Getter functions, direct from dict depending on view mode
    def get_file_path(self) -> str:
        return self.storage[self.current_mode].get_file_path()
    
    def get_frames_amount(self) -> int:
        return self.storage[self.current_mode].file_metadata["Frames"]
    
    def get_initial_x_range(self) -> float:
        return self.storage[self.current_mode].image_metadata[0]["X Range (nm)"]
    
    def get_fps_speed(self) -> float:
        return self.storage[self.current_mode].file_metadata["Speed (FPS)"]
    
    def get_line_frequency(self) -> float:
        return self.storage[self.current_mode].file_metadata["Line/s (Hz)"]
    
    def get_y_dims(self) -> int:
        return self.storage[self.current_mode].file_metadata["Y Pixel Dimensions"]
    
    def get_x_dims(self) -> int:
        return self.storage[self.current_mode].file_metadata["X Pixel Dimensions"]
    
    def get_initial_pix_nm_scaling(self) -> float:
        return self.storage[self.current_mode].image_metadata[0]["Pixel/nm Scaling Factor"]
    
    def get_cw_channel(self) -> str:
        return self.storage[self.current_mode].file_metadata["Current channel"]     

    def get_channels_list(self) -> list:
        return self.storage[self.current_mode].file_metadata["Available channels"]
    
    # Getter functions. Retrieves lists and dicts depending on view mode
    def get_file_metadata(self) -> dict:
        return self.storage[self.current_mode].file_metadata
    
    def get_frames_metadata_per_frame(self, frame_no: int) -> dict:
        return self.storage[self.current_mode].image_metadata[frame_no]
    
    def get_frames_metadata(self) -> dict:
        return self.storage[self.current_mode].image_metadata
    
    def get_frames(self) -> np.ndarray:
        return self.storage[self.current_mode].image_data
    


    def output_file_data(self, show_image_data: bool = False):
        for mode, storage in self.storage.items():
            print(f"{mode.capitalize()} Data:")
            self._output_storage_data(storage, show_image_data)
            print()
        print(f"Current mode: {self.current_mode}")

    def _output_storage_data(self, storage: MediaStorage, show_image_data: bool):
        print(f"File path: {storage.file_path}")
        print(f"File ext: {storage.file_ext}")
        print(f"File metadata: {storage.file_metadata}")
        if show_image_data:
            print(f"File image data: {storage.image_data}")
        print(f"Is in folder?: {storage.contained_in_folder}")

    # New method to add a new storage type
    def add_storage_type(self, storage_type: str):
        if storage_type not in self.storage:
            self.storage[storage_type] = MediaStorage()
        else:
            print(f"Storage type '{storage_type}' already exists.")

    # New method to remove a storage type
    def remove_storage_type(self, storage_type: str):
        if storage_type in self.storage and storage_type not in ['Target', 'Preview']:
            del self.storage[storage_type]
        else:
            print(f"Cannot remove storage type '{storage_type}'.")

    def reset(self):
        """Reset all stored data to None."""
        self.file_path = None
        self.file_ext = None
        self.file_metadata = None
        self.image_data = None
        self.image_metadata = None
        self.channels = None
        self.contained_in_folder = None
