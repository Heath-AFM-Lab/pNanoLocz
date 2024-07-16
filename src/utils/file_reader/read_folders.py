import os
from pathlib import Path
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from read_nhf import open_nhf
from read_jpk import open_jpk
from read_ibw import open_ibw
from read_spm import open_spm
from read_gwy import open_gwy
import matplotlib.colors as colors
import time  # Import the time module

AFM = np.load('AFM_cmap.npy')
AFM = colors.ListedColormap(AFM)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXPECTED_FILE_TYPES = {'.nhf', '.jpk', '.ibw', '.spm', '.gwy'}

class ImageLoader:
    def __init__(self, folder_path: str):
        self._folder_path = folder_path
        self._dominant_format, self._file_paths = self._check_folder()
        
        start_time = time.time()  # Start timing before loading images
        self._images, self._metadata = self._load_images()
        end_time = time.time()  # End timing after loading images

        self._load_time = end_time - start_time  # Calculate the duration

    def _check_folder(self):
        file_list = list(Path(self._folder_path).rglob('*'))
        file_format_count = {}

        for file_path in file_list:
            if file_path.is_file():
                ext = file_path.suffix
                if ext in EXPECTED_FILE_TYPES:
                    file_format_count[ext] = file_format_count.get(ext, 0) + 1

        if not file_format_count:
            raise ValueError("No files found with expected formats.")

        dominant_format = max(file_format_count, key=file_format_count.get)
        dominant_format_files = [str(file_path) for file_path in file_list if file_path.suffix == dominant_format]

        logger.info(f"Dominant format: {dominant_format}")
        logger.info(f"Number of files: {len(dominant_format_files)}")

        return dominant_format, dominant_format_files

    def _load_images(self):
        images = []
        metadata = None

        for file_path in self._file_paths:
            if self._dominant_format == '.nhf':
                im, meta = open_nhf(file_path, 'Topography')
            elif self._dominant_format == '.jpk':
                im, meta = open_jpk(file_path, "height_trace")
            elif self._dominant_format == '.ibw':
                im, meta = open_ibw(file_path, 1)
            elif self._dominant_format == '.spm':
                im, meta = open_spm(file_path, 1)
            elif self._dominant_format == '.gwy':
                im, meta = open_gwy(file_path, 1)
            images.append(im)
            metadata = meta  # Assume metadata is same for all images

        return images, metadata

    def get_images(self):
        return self._images

    def get_metadata(self):
        return self._metadata

    def get_load_time(self):
        return self._load_time

    def play_images(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self._images[0], animated=True, cmap=AFM)

        def updatefig(i):
            im.set_array(self._images[i])
            return im,

        ani = animation.FuncAnimation(fig, updatefig, frames=len(self._images), interval=100, blit=True)
        plt.show()

if __name__ == "__main__":
    folder_path = 'data/Streptavidin imaging-12.08.46.399'  # Replace with folder path
    image_loader = ImageLoader(folder_path)
    print(f"Time taken to load images: {image_loader.get_load_time()} seconds")
    image_loader.play_images()
