from typing import Tuple
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from utils.constants import DEPTH_CONTROL_OPTIONS

class DepthControlManager(QObject):
    update_widgets = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.depth_control_type = DEPTH_CONTROL_OPTIONS[0]
        self.frame_depth_metadata_dict = {}
        self.manual_min = 0.0
        self.manual_max = 0.0

    def get_depth_control_type(self, name: str):
        self.depth_control_type = name
        self.update_widgets.emit()

    def load_depth_control_data(self, frames: np.ndarray, frame_metadata: dict):
        self.reset()
        for frame_no in range(len(frames)):
            max_frame_value = frame_metadata[frame_no]["Max pixel value"]
            min_frame_value = frame_metadata[frame_no]["Min pixel value"]
            min_outlier_frame_value, max_outlier_frame_value = self._calculate_outlier_bounds(frames[frame_no])
            # TODO: complete function for the Histogram min max values (requires histogram to use)
            min_histogram_frame_value, max_histogram_frame_value = self._calculate_histogram_bounds(frames[frame_no])

            # Storing the values in a nested dictionary structure
            self.frame_depth_metadata_dict[frame_no] = {
                "Frame": {
                    "Min": min_frame_value,
                    "Max": max_frame_value
                },
                "Outlier": {
                    "Min": min_outlier_frame_value,
                    "Max": max_outlier_frame_value
                },
                "Histogram": {
                    "Min": min_histogram_frame_value,
                    "Max": max_histogram_frame_value
                }
            }
            print(min_outlier_frame_value, max_outlier_frame_value)
        print(frames.shape)

    def get_min_max_depths_per_frame(self, frame_no: int) -> Tuple[float, float]:
        if self.depth_control_type == DEPTH_CONTROL_OPTIONS[0]:
            # Frames min max
            return self.frame_depth_metadata_dict[frame_no]["Frame"]["Min"], self.frame_depth_metadata_dict[frame_no]["Frame"]["Max"]
        elif self.depth_control_type == DEPTH_CONTROL_OPTIONS[1]:
            # Histogram min max
            return self.frame_depth_metadata_dict[frame_no]["Histogram"]["Min"], self.frame_depth_metadata_dict[frame_no]["Histogram"]["Max"]
        elif self.depth_control_type == DEPTH_CONTROL_OPTIONS[2]:
            # Outliers min max
            return self.frame_depth_metadata_dict[frame_no]["Outlier"]["Min"], self.frame_depth_metadata_dict[frame_no]["Outlier"]["Max"]
        elif self.depth_control_type == DEPTH_CONTROL_OPTIONS[3]:
            # Manual min max
            return self.manual_min, self.manual_max 
        else:
            raise ValueError(f"Unknown depth control type: {self.depth_control_type}")

    def get_min_max_manual_values(self, min_value: float, max_value: float):
        self.manual_min = min_value
        self.manual_max = max_value
        self.update_widgets.emit()


    def _calculate_outlier_bounds(self, frame: np.ndarray) -> Tuple[float, float]:

        if np.isnan(frame).any():
            print("Warning: NaN values detected in the frame.")
        if np.isinf(frame).any():
            print("Warning: Infinite values detected in the frame.")

        mean = np.mean(frame)
        std_dev = np.std(frame)
        print(frame)
        lower_bound = mean - 3 * std_dev
        upper_bound = mean + 3 * std_dev
        print(mean, std_dev)
        print(frame.shape)
        return lower_bound, upper_bound
    
    # TODO: complete function for the Histogram min max values (requires histogram to use)
    def _calculate_histogram_bounds(self, frame: np.ndarray) -> Tuple[float, float]:
        return 0.0, 0.0
    
    def reset(self):
        self.frame_depth_metadata_dict = {}

