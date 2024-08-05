import os
from collections import Counter
import numpy as np
from .read_folders import ImageLoader
from .asd import load_asd
from .read_aris import open_aris
from .read_ibw import open_ibw
from .read_jpk import open_jpk
from .read_nhf import open_nhf
from .read_spm import open_spm
from .read_gwy import open_gwy
from core.Image_Storage_Class import MediaDataManager


def loadFileData(file_path, channel = None):
    # Instantiate core media manager class
    media_data_manager = MediaDataManager()
    if os.path.isdir(file_path):
        image_loader = ImageLoader(file_path)#
        dominant_format = image_loader.get_dominant_format()
        if dominant_format is not None:  # Only display data if criteria met
            frames = [data['image'] for data in image_loader._data_dict.values()]
            metadata = [data['metadata'] for data in image_loader._data_dict.values()]
            channels = [data['channels'] for data in image_loader._data_dict.values()]

            # Eliminate repeating channel names
            # Takes a the set of channels from an image and compares it to the next
            # Eliminates channels that does not appear across all frames/images
            repeating_channels = []
            for frame_number, frame_channels in enumerate(channels):
                if frame_number == 0:
                    repeating_channels = frame_channels
                    continue

                # Counter of the current repeating_channels
                counter1 = Counter(repeating_channels)
                # Counter of the current frame_channels
                counter2 = Counter(frame_channels)
                
                # Intersection with counts
                common_counter = counter1 & counter2
                
                # Convert the common elements counter to a list
                repeating_channels = list(common_counter.elements())

            if '' in repeating_channels:
                repeating_channels.remove('')

            media_data_manager.load_new_folder_data(folder_path=file_path, dominant_file_ext=dominant_format, frames=frames,
                                            folder_metadata=metadata, channels=repeating_channels)

            # self.displayDataFolders(frames, metadata, file_path)
        else:
            print("Folder does not meet the criteria for image series.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.asd':
        frames, metadata, channels = load_asd(file_path, channel)  
    elif ext == '.aris':
        frames, metadata, channels = open_aris(file_path, channel)
    elif ext == '.ibw':
        frames, metadata, channels = open_ibw(file_path, channel)
    elif ext == '.jpk':
        frames, metadata, channels = open_jpk(file_path, channel)
    elif ext == '.nhf':
        frames, metadata, channels = open_nhf(file_path, channel)
    elif ext == '.spm':
        frames, metadata, channels = open_spm(file_path, channel)
    elif ext == '.gwy':
        frames, metadata, channels = open_gwy(file_path, channel)
    else:
        print(f"Unsupported file type: {ext}")
        return
    
    if '' in channels:
        channels.remove('')
    
    media_data_manager.load_new_file_data(file_path=file_path, file_ext=ext, frames=frames,
                                            file_metadata=metadata, channels=channels)