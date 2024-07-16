import h5py
import numpy as np
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors

AFM = np.load('AFM_cmap.npy')
AFM = colors.ListedColormap(AFM)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def explore_h5py_group(group, path=''):
    for key in group.keys():
        item = group[key]
        logger.info(f"Found {type(item)}: {path}/{key}")
        if isinstance(item, h5py.Group):
            explore_h5py_group(item, path=f"{path}/{key}")
        elif isinstance(item, h5py.Dataset):
            logger.info(f"Dataset shape: {item.shape}")

def open_aris(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict]:
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
    tuple[np.ndarray, dict]
        A tuple containing the image and its metadata.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    ValueError
        If the channel is not found in the .aris file.
    """
    logger.info(f"Loading image from: {file_path}")
    file_path = Path(file_path)
    
    try:
        with h5py.File(file_path, 'r') as file:
            # logger.info("Exploring file structure...")
            # explore_h5py_group(file)

            info = file['/DataSet']
            datainfo = file['/DataSetInfo']

            Framename = [key for key in info['Resolution 0'].keys() if 'Frame ' in key]
            newStr = [name.split('Frame ')[-1] for name in Framename]
            X = list(map(int, newStr))
            M = sorted(range(len(X)), key=lambda k: X[k])

            logger.info(f"Frame names: {Framename}")
            logger.info(f"Frame indices: {X}")
            logger.info(f"Sorted indices: {M}")

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
            logger.info(f"DimScaling: {dim_scaling}")
            if isinstance(dim_scaling, np.ndarray):
                scale0 = np.max(dim_scaling)
            else:
                scale0 = dim_scaling
            logger.info(f"Initial scale: {scale0}")

            scan_size_list = datainfo['Frames']
            scan_size_frame = []
            ScanSize = []

            logger.info(f"Scan size list length: {len(scan_size_list)}")
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

            logger.info(f"Scan size frames: {scan_size_frame}")
            logger.info(f"Scan sizes: {ScanSize}")

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

            logger.info(f"Scales: {s['scale']}")

            # Log all available attributes in DataSetInfo
            logger.info(f"Available attributes in DataSetInfo: {list(datainfo.attrs.keys())}")
            for key in datainfo.attrs.keys():
                logger.info(f"{key}: {datainfo.attrs[key]}")

            # Locate attributes for yPixel, xPixel, and frameAcqTime
            s['yPixel'] = datainfo.attrs.get('ScanLines', None)
            s['xPixel'] = datainfo.attrs.get('ScanPoints', None)
            s['frameAcqTime'] = datainfo.attrs.get('TimePerFrame', 0)

            # Dynamically determine yPixel and xPixel from the first frame's shape
            if s['yPixel'] is None or s['xPixel'] is None:
                first_frame_loc = f'/DataSet/Resolution 0/Frame {X[M[0]]}/{channel}/Image'
                first_frame_shape = file[first_frame_loc].shape
                s['yPixel'], s['xPixel'] = first_frame_shape
                logger.info(f"Dynamically determined yPixel: {s['yPixel']}, xPixel: {s['xPixel']}")

            s['numberofFrames'] = len(M)

            # Load Images
            im = np.zeros((s['yPixel'], s['xPixel'], s['numberofFrames']))
            for i in range(len(M)):
                img_loc = f'/DataSet/Resolution 0/Frame {X[M[i]]}'
                im[:, :, i] = file[f'{img_loc}/{channel}/Image'][()].T

            im[np.isnan(im)] = 0

    except FileNotFoundError:
        logger.error(f"[{file_path}] File not found: {file_path}")
        raise
    except KeyError as e:
        logger.error(f"Attribute not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        raise

    return im, s

if __name__ == "__main__":
    file_path = 'data/00T2_P3_0000.ARIS'
    channel = 'HeightTrace'  # Replace with the appropriate channel name
    try:
        image, info = open_aris(file_path, channel)
        print(f"Metadata: {info}")
        print(f"Image shape: {image.shape}")
        
        # Display the image using matplotlib
        if image.ndim == 2:
            plt.imshow(image, cmap=AFM)
            plt.colorbar(label='Height (nm)')
            plt.show()
        elif image.ndim == 3:
            fig, ax = plt.subplots()
            frame_image = ax.imshow(image[:, :, 0], cmap=AFM)

            def update_frame(frame_number):
                frame_image.set_data(image[:, :, frame_number])
                return frame_image,

            ani = animation.FuncAnimation(fig, update_frame, frames=image.shape[2], interval=50, blit=True)
            plt.show()
        else:
            print("Unsupported image dimensions.")
    except Exception as e:
        print(f"Error: {e}")
