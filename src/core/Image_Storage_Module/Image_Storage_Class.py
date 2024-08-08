import numpy as np
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from collections import Counter
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

        # Control classes to handle frame data
        # self.depth_control_manager = DepthControlManager()

    def __init__(self):
        # This method is now empty to avoid re-initialization
        pass

    def load_new_file_data(self, file_path: str, file_ext: str, frames: np.ndarray | list | tuple, 
                           file_metadata: list, channels: list):
        """Load new file data into the manager, resetting previous data."""
        # Reset all variables
        self.reset()

        # Convert frames to np.array if not already
        if isinstance(frames, (list, tuple)):
            frames = np.array(frames, dtype=np.float32)
        
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
        # Store frames metadata
        for frame_no in range(file_metadata["Frames"]):
            frame_metadata_values = [
                file_metadata["X Range (nm)"],
                file_metadata["Pixel/nm Scaling Factor"],
                np.max(frames[frame_no]),
                np.min(frames[frame_no]),
                file_metadata["Timestamp"][frame_no] if file_metadata["Frames"] != 1 else 0
            ]
            frame_metadata_dictionary[frame_no] = dict(zip(IMAGE_METADATA_DICT_KEYS, frame_metadata_values))

        # Store the rest of the variables to the class
        self.file_path = file_path
        self.file_ext = file_ext
        self.file_metadata = dict(zip(FILE_METADATA_DICT_KEYS, file_metadata_values))
        self.image_data = frames
        self.image_metadata = frame_metadata_dictionary
        self.contained_in_folder = False

        self.new_file_loaded.emit()
        self.output_file_data()

    def load_new_folder_data(self, folder_path: str, dominant_file_ext: str, frames: np.ndarray | list | tuple, 
                             folder_metadata: list, channels: list):
        """Load new folder data into the manager, resetting previous data."""
        # Reset all variables
        self.reset()

        # Convert frames to np.array if not already
        if isinstance(frames, (list, tuple)):
            try:
                # Dont change the dtype to float 16 in an effort to save memory, 
                # It causes errors with calculating std dev
                frames = np.array(frames, dtype=np.float32)
            except ValueError:
                frames, folder_metadata = self._filter_arrays_by_common_shape(frames, folder_metadata)
                # print(len(frames), folder_metadata)

        if frames.ndim not in [2, 3]:
            raise ValueError("Frames must be a 2D or 3D array.")
        
        # Add a new axis to handle images as if they are frames
        if frames.ndim == 2:
            frames = np.expand_dims(frames, axis=0)

        if len(folder_metadata[0]) != len(STANDARDISED_METADATA_DICT_KEYS):
            print(len(folder_metadata[0]), len(STANDARDISED_METADATA_DICT_KEYS))
            raise ValueError("The length of folder_metadata does not match the required metadata keys.")
        
        # Run checks across all metadata from each file. TODO
        # Store file metadata
        file_metadata_values = [
            len(frames),
            folder_metadata[0]["Speed (FPS)"],
            folder_metadata[0]["Line/s (Hz)"],
            folder_metadata[0]["Y Pixel Dimensions"],
            folder_metadata[0]["X Pixel Dimensions"],
            folder_metadata[0]["Current channel"],
            channels
        ]

        for index, metadata_value in enumerate(folder_metadata):
            if (file_metadata_values[1] != metadata_value["Speed (FPS)"] or
                file_metadata_values[2] != metadata_value["Line/s (Hz)"] or
                file_metadata_values[3] != metadata_value["Y Pixel Dimensions"] or
                file_metadata_values[4] != metadata_value["X Pixel Dimensions"] or
                file_metadata_values[5] != metadata_value["Current channel"]
                ):
                # Create a message box instance
                msg_box = QMessageBox()

                # Set the icon, title, and text for the message box
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("File metadata inconsistency")
                msg_box.setText("File metadata does not match across all files inside selected folder. This may be because a file with the same file extension exists inside this folder that does not belong in there")

                # Set detailed text if needed
                msg_box.setInformativeText("Click OK to proceed unloading the images. Doing so may result in undefined behaviour e.g. Crashing the program.")

                # Add standard buttons to the message box
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

                # Show the message box
                response = msg_box.exec()

                print(metadata_value, index)
                print(file_metadata_values)

                # Handle the response
                if response == QMessageBox.StandardButton.Ok:
                    break
                else:
                    self.reset()
                    return
                
                

        frame_metadata_dictionary = {}
        # Store frames metadata
        for frame_no in range(len(frames)):
            frame_metadata_values = [
                folder_metadata[frame_no]["X Range (nm)"],
                folder_metadata[frame_no]["Pixel/nm Scaling Factor"],
                np.max(frames[frame_no]),
                np.min(frames[frame_no]),
                folder_metadata[frame_no]["Timestamp"]
            ]
            frame_metadata_dictionary[frame_no] = dict(zip(IMAGE_METADATA_DICT_KEYS, frame_metadata_values))

        # Store the rest of the variables to the class
        self.file_path = folder_path
        self.file_ext = dominant_file_ext
        self.file_metadata = dict(zip(FILE_METADATA_DICT_KEYS, file_metadata_values))
        self.image_data = frames
        self.image_metadata = frame_metadata_dictionary
        self.contained_in_folder = True

        self.new_file_loaded.emit()
        self.output_file_data()

    @staticmethod
    def _filter_arrays_by_common_shape(arrays, metadata):
        """
        Filters a list of 2D numpy arrays, keeping only those with the most common shape.
        
        Parameters:
        arrays (list of np.ndarray): List of 2D numpy arrays.
        metadata (list of dict): List of metadata dictionaries corresponding to each array.
        
        Returns:
        tuple: Filtered list of arrays with the most common shape, filtered metadata, and the indices of the removed arrays.
        """
        # Get the shape of each array
        shapes = [arr.shape for arr in arrays]
        
        # Find the most common shape
        shape_counts = Counter(shapes)
        most_common_shape = shape_counts.most_common(1)[0][0]
        
        # Filter the arrays and metadata to keep only those with the most common shape
        filtered_arrays = []
        filtered_metadata = []
        for i, (arr, md) in enumerate(zip(arrays, metadata)):
            if arr.shape == most_common_shape:
                filtered_arrays.append(arr)
                filtered_metadata.append(md)
        
        return np.array(filtered_arrays), filtered_metadata
    

    # def get_frame_min_max(self) -> Tuple[float, float]:
        
        
    
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
