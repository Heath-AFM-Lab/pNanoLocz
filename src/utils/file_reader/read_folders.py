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
                dominant_format_files = [str(file_path) for file_path in file_list if file_path.suffix == dominant_format]
                break


        return dominant_format, dominant_format_files
    
    def get_load_time(self):
        return self._load_time

    def _load_images(self):
        data_dict = {}

        for file_path in self._file_paths:
            if self._dominant_format == '.nhf':
                im, meta, channels = open_nhf(file_path, 'Topography')
            elif self._dominant_format == '.jpk':
                im, meta, channels = open_jpk(file_path, "height_trace")
            elif self._dominant_format == '.ibw':
                im, meta, channels = open_ibw(file_path, 1)
            elif self._dominant_format == '.spm':
                im, meta, channels = open_spm(file_path, "Height")
            elif self._dominant_format == '.gwy':
                im, meta, channels = open_gwy(file_path, 1)
            meta["Frames"] = len(self._file_paths)

            data_dict[file_path] = {'image': im, 'metadata': meta, 'channels': channels}

        return data_dict
    
    def get_dominant_format(self) -> str:
        return self._dominant_format
