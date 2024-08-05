import h5py
import numpy as np
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils.constants import STANDARDISED_METADATA_DICT_KEYS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def open_aris(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict, list]:
    """
    Extract image and metadata from the ARIS file.

    Parameters
    ----------
    file_path : Path or str
        Path to the .aris file.
    channel : str
        Channel name to extract from the .aris file.

    Returns
    -------
    tuple[np.ndarray, dict, list]
        A tuple containing the image, its metadata, and parameter values.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    ValueError
        If the channel is not found in the .aris file.
    """
    file_path = Path(file_path)
    
    try:
        with h5py.File(file_path, 'r') as file:
            # Explore file structure to identify where metadata might be stored

            info = file['/DataSet']
            datainfo = file['/DataSetInfo']

            Framename = [key for key in info['Resolution 0'].keys() if 'Frame ' in key]
            newStr = [name.split('Frame ')[-1] for name in Framename]
            X = list(map(int, newStr))
            M = sorted(range(len(X)), key=lambda k: X[k])

            ch_info = file['/DataSetInfo/Global/Channels']
            found_ch = False
            s = {'channels': []}
            for ch_group in ch_info.keys():
                ch_name = ch_group.split('/')[-1]
                s['channels'].append(ch_name)
                if channel == ch_name:
                    found_ch = True

            if not found_ch:
                s['channel'] = 'HeightTrace'
                channel = 'HeightTrace'
            else:
                s['channel'] = channel

            dim_scaling = file['/DataSetInfo/Global/Channels/HeightTrace/ImageDims'].attrs['DimScaling']
            if isinstance(dim_scaling, np.ndarray):
                scale0 = np.max(dim_scaling)
            else:
                scale0 = dim_scaling

            scan_size_list = datainfo['Frames']
            scan_size_frame = []
            ScanSize = []

            for frame in scan_size_list:
                try:
                    if isinstance(frame, h5py.Group):
                        temp = frame.name.split('Frame ')[-1]
                        scan_size_frame.append(int(temp))
                        temp_attrs = frame['Channels/HeightTrace/ImageDims'].attrs
                        ScanSize.append(temp_attrs['ScanSize'])
                except Exception as e:
                    logger.error(f"Error processing frame {frame}: {e}")

            scan_size_frame = [x for x in scan_size_frame if x != 0]
            ScanSize = [x for x in ScanSize if x != 0]

            if len(scan_size_frame) > 0:
                Scale_sortV, Scale_sortID = zip(*sorted(zip(scan_size_frame, range(len(scan_size_frame)))))
            else:
                Scale_sortV, Scale_sortID = [], []

            s['scale'] = []
            for i in range(len(X)):
                if i == 0:
                    s['scale'].append(scale0)
                else:
                    if len(Scale_sortV) > 0:
                        if i < Scale_sortV[0]:
                            s['scale'].append(s['scale'][-1])
                        else:
                            s['scale'].append(ScanSize[Scale_sortID[0]])
                            Scale_sortV = Scale_sortV[1:]
                            Scale_sortID = Scale_sortID[1:]
                    else:
                        s['scale'].append(s['scale'][-1])

            # Check frame-specific parameters for timing
            first_frame_path = f'/DataSetInfo/Frames/Frame {X[M[0]]}/Parameters/Scan'

            # Attempt to read frame acquisition time from specific parameters
            s['yPixel'] = datainfo.attrs.get('ScanLines', None)
            s['xPixel'] = datainfo.attrs.get('ScanPoints', None)
            
            # Calculate FPS from frame acquisition time
            fps = 1

            # Dynamically determine yPixel and xPixel from the first frame's shape
            if s['yPixel'] is None or s['xPixel'] is None:
                first_frame_loc = f'/DataSet/Resolution 0/Frame {X[M[0]]}/{channel}/Image'
                first_frame_shape = file[first_frame_loc].shape
                s['yPixel'], s['xPixel'] = first_frame_shape

            s['numberofFrames'] = len(M)

            # Load Images and attach timestamps
            im = np.zeros((s['yPixel'], s['xPixel'], s['numberofFrames']))
            metadata_list = []  # List to store metadata including timestamps for each frame

            # Calculate timestamps for each frame
            # Try accessing the Series Time dataset for timing information
            try:
                time_series = file['/DataSetInfo/Series/Time']
                time_stamps = np.array(time_series)
            except KeyError as e:
                print(f"Time Series not found: {e}")
                time_stamps = np.arange(s['numberofFrames'])  # Default to sequential if missing

            # Compute FPS if timestamps are available
            if len(time_stamps) > 1:
                frame_interval = time_stamps[1] - time_stamps[0]  # Time difference between the first two frames
                fps = 1.0 / frame_interval if frame_interval > 0 else 1.0  # Prevent division by zero

            for i in range(len(M)):
                img_loc = f'/DataSet/Resolution 0/Frame {X[M[i]]}'
                image_data = file[f'{img_loc}/{channel}/Image'][()]
                
                # Check the shape of the image data before transposing
                if image_data.shape != (s['xPixel'], s['yPixel']):
                    image_data.shape = (s['xPixel'], s['yPixel'])
                    image_data = image_data.T

                im[:, :, i] = image_data

                # Create metadata entry for each frame
                frame_metadata = {
                    'frame_index': i,
                    'timestamp': time_stamps[i],
                    'scaling': s['scale'][i],
                    'channel': channel
                }
                metadata_list.append(frame_metadata)

            im[np.isnan(im)] = 0

            # Calculate additional parameters
            line_rate = s['yPixel'] * fps if s['yPixel'] else 0
            pixel_to_nanometre_scaling_factor = 1 / np.max(dim_scaling) if np.any(dim_scaling) else 0

            values = [
                s.get('numberofFrames', 'N/A'),
                (np.max(dim_scaling) if np.any(dim_scaling) else 'N/A'),
                fps,
                line_rate,
                s.get('yPixel', 'N/A'),
                s.get('xPixel', 'N/A'),
                pixel_to_nanometre_scaling_factor,
                channel,
                ""
            ]

            if len(values) != len(STANDARDISED_METADATA_DICT_KEYS):
                raise ValueError(f"The length of the values in .ARIS does not match the required metadata keys.")

            # Create the metadata dictionary
            file_metadata = dict(zip(STANDARDISED_METADATA_DICT_KEYS, values))
            file_metadata['frames'] = metadata_list  # Store all frame metadata in the dictionary

            channels = s['channels']

    except FileNotFoundError:
        logger.error(f"[{file_path}] File not found: {file_path}")
        raise
    except KeyError as e:
        logger.error(f"Attribute not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        raise

    return im, file_metadata, channels

if __name__ == "__main__":
    file_path = 'data/00T2_P3_0000.ARIS'
    channel = 'HeightTrace'  # Replace with the appropriate channel name
    try:
        image, info, values = open_aris(file_path, channel)
        print(f"Metadata: {info}")
        print(f"Image shape: {image.shape}")
        print(f"Parameter values: {values}")
        
        # Display the image using matplotlib
        if image.ndim == 2:
            plt.imshow(image, cmap='gray')
            plt.colorbar(label='Height (nm)')
            plt.show()
        elif image.ndim == 3:
            fig, ax = plt.subplots()
            frame_image = ax.imshow(image[:, :, 0], cmap='gray')

            def update_frame(frame_number):
                frame_image.set_data(image[:, :, frame_number])
                ax.set_title(f"Time: {info['frames'][frame_number]['timestamp']:.2f} s")
                return frame_image,

            ani = animation.FuncAnimation(fig, update_frame, frames=image.shape[2], interval=1000 * (info['frames'][1]['timestamp'] - info['frames'][0]['timestamp']), blit=True)
            plt.show()
        else:
            print("Unsupported image dimensions.")
    except Exception as e:
        print(f"Error: {e}")
