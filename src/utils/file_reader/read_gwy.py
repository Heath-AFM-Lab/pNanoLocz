from __future__ import annotations
from pathlib import Path
import struct
import numpy as np
import logging
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils.constants import STANDARDISED_METADATA_DICT_KEYS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_str(f):
    result = bytearray()
    while True:
        char = f.read(1)
        if char == b'\x00':
            break
        result.extend(char)
    return result.decode('utf-8')

def read_component(f):
    name = read_str(f)
    dtype = f.read(1).decode('utf-8')

    if dtype == 'b':
        value = struct.unpack('<B', f.read(1))[0]
    elif dtype == 'c':
        value = f.read(1).decode('utf-8')
    elif dtype == 'i':
        value = struct.unpack('<i', f.read(4))[0]
    elif dtype == 'q':
        value = struct.unpack('<q', f.read(8))[0]
    elif dtype == 'd':
        value = struct.unpack('<d', f.read(8))[0]
    elif dtype == 's':
        value = read_str(f)
    elif dtype == 'o':
        sub_obj_name = read_str(f)
        sub_obj_size = struct.unpack('<I', f.read(4))[0]
        value = read_object(f, sub_obj_size)
    elif dtype == 'D':
        size = struct.unpack('<I', f.read(4))[0]
        value = np.frombuffer(f.read(size * 8), dtype=np.float64)
    elif dtype == 'S':  # Handling 'S' type for strings
        length = struct.unpack('<I', f.read(4))[0]
        value = f.read(length).decode('utf-8')
    elif dtype == 'p':  # Handling 'p' type for binary data
        length = struct.unpack('<I', f.read(4))[0]
        value = f.read(length)
    else:
        raise ValueError(f"Unsupported data type: {dtype}")

    return name, dtype, value

def read_object(f, size):
    obj = {}
    start_pos = f.tell()
    while f.tell() - start_pos < size:
        name, dtype, value = read_component(f)
        obj[name] = value
    return obj

def read_datafield(f, size):
    datafield = {}
    start_pos = f.tell()
    while f.tell() - start_pos < size:
        name, dtype, value = read_component(f)
        datafield[name] = value

    xres = datafield['xres']
    yres = datafield['yres']
    data = datafield['data'].reshape((yres, xres)).T
    datafield['data'] = data
    return datafield

def open_gwy(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict, list]:
    """
    Extract image and metadata from the GWY file.

    Parameters
    ----------
    file_path : Path or str
        Path to the .gwy file.
    channel : str
        Channel name to extract from the .gwy file.

    Returns
    -------
    tuple[np.ndarray, dict, list]
        A tuple containing the image, its metadata, and parameter values.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    ValueError
        If the channel is not found in the .gwy file.
    """
    # logger.info(f"Loading image from: {file_path}")
    file_path = Path(file_path)
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4).decode('utf-8')
            if header != 'GWYP':
                raise ValueError("Not a valid GWY file")

            root_obj = read_str(f)
            root_size = struct.unpack('<I', f.read(4))[0]
            if root_obj != 'GwyContainer':
                raise ValueError("Not a valid GwyContainer object")

            channels = []
            channel_meta = []
            while f.tell() < root_size:
                name, dtype, value = read_component(f)
                if dtype == 'o' and isinstance(value, dict) and 'data' in value:
                    ch_no = int(name.split('/')[1])
                    channels.append((ch_no, name))
                    channel_meta.append(value)

            # logger.info(f"Found channels: {channels}")

            # Ensure correct reshaping of image data
            for meta in channel_meta:
                xres = meta['xres']
                yres = meta['yres']
                meta['data'] = meta['data'].reshape((yres, xres)).T

            # Filter images for the specified channel
            channel_indices = [i for i, (_, name) in enumerate(channels) if f'/{channel}/data' in name]
            if not channel_indices:
                # logger.warning(f"Channel '{channel}' not found. Using the first available channel instead.")
                channel_indices = [0]  # Use the first available channel
            
            images = [channel_meta[i]['data'] for i in channel_indices]
            meta = channel_meta[channel_indices[0]] if channel_indices else {}
            if 'data' in meta:
                meta.pop('data')
            meta['channels'] = [channels[channel_indices[0]][1].split('/')[1]]  # Update the channel name

            # Flip the image vertically and convert to nm
            images = [np.flipud(image) for image in images]
            images = [np.rot90(image, k=3) for image in images]
            images = np.array(images) * 1e9
            

            # Calculate additional values
            num_frames = len(images)
            y_pixels, x_pixels = images[0].shape
            x_range_nm = float(meta['xreal']) * 1e9  # Convert to nm
            scan_rate = meta.get('scan_rate', 0)
            fps = 1 / scan_rate if scan_rate != 0 else 0
            line_rate = y_pixels * fps if y_pixels else 0
            pixel_to_nanometre_scaling_factor = x_pixels / x_range_nm 

            values = [
                num_frames,
                x_range_nm,
                fps,
                line_rate,
                y_pixels,
                x_pixels,
                pixel_to_nanometre_scaling_factor,
                meta['channels'][0],
                None
            ]

            if len(values) != len(STANDARDISED_METADATA_DICT_KEYS):
                raise ValueError(f"The length of the values in .gwy does not match the required metadata keys.")

            # Create the metadata dictionary
            file_metadata = dict(zip(STANDARDISED_METADATA_DICT_KEYS, values))
            

            return images, file_metadata, meta['channels']

    except FileNotFoundError:
        logger.error(f"[{file_path}] File not found: {file_path}")
        raise
    except KeyError as e:
        logger.error(f"Attribute not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        raise

if __name__ == "__main__":
    file_path = 'data/SBS-PS_example_data.gwy'
    channel = 'None'  # Replace with the appropriate channel name
    try:
        images, meta, values = open_gwy(file_path, channel)
        print(f"Metadata: {meta}")
        print(f"Parameter values: {values}")
        for i, img in enumerate(images):
            print(f"Channel {i} image shape: {img.shape}")

        # Display the image using matplotlib
        if len(images) == 1:
            plt.imshow(images[0], cmap=AFM)
            plt.colorbar(label='Height (nm)')
            plt.show()
        elif len(images) > 1:
            fig, ax = plt.subplots()
            frame_image = ax.imshow(images[0], cmap=AFM)

            def update_frame(frame_number):
                frame_image.set_data(images[frame_number])
                return frame_image,

            ani = animation.FuncAnimation(fig, update_frame, frames=len(images), interval=50, blit=True)
            plt.show()
        else:
            print("No images found.")
    except Exception as e:
        print(f"Error: {e}")
