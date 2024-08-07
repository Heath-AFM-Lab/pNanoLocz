from pathlib import Path
import logging
from utils.file_reader.read_ibw import open_ibw
from utils.file_reader.read_jpk import open_jpk
from utils.file_reader.read_nhf import open_nhf
from utils.file_reader.read_spm import open_spm
from utils.file_reader.read_gwy import open_gwy
import time
from utils.constants import IMG_EXTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageLoader:
    def __init__(self, folder_path: str):
        self._folder_path = folder_path
        self._dominant_format, self._file_paths = self._check_folder()
        
        if self._dominant_format is not None:  # Only proceed if criteria met
            start_time = time.time()  # Start timing before loading images
            self._data_dict = self._load_images()
            end_time = time.time()  # End timing after loading images

            self._load_time = end_time - start_time  # Calculate the duration
        else:
            self._data_dict = {}
            self._load_time = 0

    def _check_folder(self):
        file_list = list(Path(self._folder_path).glob('*'))  # Only look at files directly inside the folder
        file_format_count = {}

        for file_path in file_list:
            if file_path.is_file():
                ext = file_path.suffix
                if ext in IMG_EXTS:
                    file_format_count[ext] = file_format_count.get(ext, 0) + 1

        dominant_format = None
        dominant_format_files = []

        for ext, count in file_format_count.items():
            if count >= 10 and all(other_count < 6 for other_ext, other_count in file_format_count.items() if other_ext != ext):
                dominant_format = ext
                # Sort the files by name in ascending order
                dominant_format_files = sorted([str(file_path) for file_path in file_list if file_path.suffix == dominant_format])
                break

        return dominant_format, dominant_format_files
    
    def get_load_time(self):
        return self._load_time

    def _load_images(self):
        data_dict = {}
        time_stamps = []
        elapsed_time = 0

        for file_path in self._file_paths:
            if self._dominant_format == '.nhf':
                im, meta, channels = open_nhf(file_path, 'Topography')
                # Calculate elapsed time for NHF files
                fps = meta.get('Speed (FPS)', 0)
                if fps > 0:
                    meta['Timestamp'] = elapsed_time
                    elapsed_time += 1 / fps
                else:
                    meta['Timestamp'] = elapsed_time
                time_stamps.append(meta['Timestamp'])
            elif self._dominant_format == '.jpk':
                im, meta, channels = open_jpk(file_path, "height_trace")
                # Calculate elapsed time for JPK files
                fps = meta.get('Speed (FPS)', 0)
                if fps > 0:
                    meta['Timestamp'] = elapsed_time
                    elapsed_time += 1 / fps
                else:
                    meta['Timestamp'] = elapsed_time
                time_stamps.append(meta['Timestamp'])
            elif self._dominant_format == '.ibw':
                im, meta, channels = open_ibw(file_path, 1)
                # Calculate elapsed time for IBW files
                fps = meta.get('Speed (FPS)', 0)
                if fps > 0:
                    meta['Timestamp'] = elapsed_time
                    elapsed_time += 1 / fps
                else:
                    meta['Timestamp'] = elapsed_time
                time_stamps.append(meta['Timestamp'])
            elif self._dominant_format == '.spm':
                im, meta, channels = open_spm(file_path, "Height")
                time_stamps.append(meta['Timestamp'])  # Extract timestamp from metadata
            elif self._dominant_format == '.gwy':
                im, meta, channels = open_gwy(file_path, 1)
                # Calculate elapsed time for GWY files
                fps = meta.get('Speed (FPS)', 0)
                if fps > 0:
                    meta['Timestamp'] = elapsed_time
                    elapsed_time += 1 / fps
                else:
                    meta['Timestamp'] = elapsed_time
                time_stamps.append(meta['Timestamp'])
            meta['Frames'] = len(self._file_paths)
            data_dict[file_path] = {'image': im, 'metadata': meta, 'channels': channels}

        if self._dominant_format == '.spm':
            elapsed_times = self._convert_to_elapsed_time(time_stamps)
            for i, file_path in enumerate(self._file_paths):
                data_dict[file_path]['metadata']['Timestamp'] = elapsed_times[i]

        return data_dict
    
    def _convert_to_elapsed_time(self, time_stamps):
        timestamps = []

        # Convert each time.struct_time object to a timestamp
        for time_struct in time_stamps:
            if isinstance(time_struct, time.struct_time):
                timestamp = time.mktime(time_struct)
                timestamps.append(timestamp)
            else:
                print(f"Unsupported type in time_stamps: {type(time_struct)}. Expected time.struct_time.")
                continue

        if not timestamps:
            print("No valid timestamps found.")
            return []

        # Calculate the elapsed times relative to the first timestamp
        elapsed_times = [t - timestamps[0] for t in timestamps]
        
        return elapsed_times
    
    def get_dominant_format(self) -> str:
        return self._dominant_format