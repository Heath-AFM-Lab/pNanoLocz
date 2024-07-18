import h5py
import numpy as np
import logging
from pathlib import Path
import matplotlib.colors as colors

AFM = np.load('utils/file_reader/AFM_cmap.npy')
AFM = colors.ListedColormap(AFM)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def open_nhf(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict, list]:
    """
    Extract image and metadata from the NHF file.

    Parameters
    ----------
    file_path : Path or str
        Path to the .nhf file.
    channel : str
        Channel name to extract from the .nhf file.

    Returns
    -------
    tuple[np.ndarray, dict, list]
        A tuple containing the image, its metadata, and parameter values.
    """
    logger.info(f"Loading image from: {file_path}")
    file_path = Path(file_path)

    with h5py.File(file_path, 'r') as f:
        # Scan attributes
        scan_attrs = f['/measurement_0'].attrs
        scan_size = scan_attrs['image_size_x']
        x_pixel = scan_attrs['image_points_per_line']
        y_pixel = scan_attrs.get('image_number_of_lines', scan_attrs.get('image_number_of_lines_aquired'))
        line_rate = scan_attrs['image_line_rate']
        frame_acq_time = y_pixel / line_rate

        s = {
            'ScanSize': scan_size,
            'xPixel': x_pixel,
            'yPixel': y_pixel,
            'linerate': line_rate,
            'frameAcqTime': frame_acq_time
        }

        # Find the dataset corresponding to the channel
        group = f['/measurement_0/segment_0']
        datasets = [ds for ds in group.keys() if ds.startswith('data')]

        # List all available channels
        available_channels = [group[ds].attrs.get('name') for ds in datasets]
        logger.info(f"Available channels: {available_channels}")
        
        if channel not in available_channels:
            channel = available_channels[0]

        for ds in datasets:
            attrs = group[ds].attrs
            if attrs.get('name') == channel:
                dataset_name = ds
                break
        else:
            raise ValueError(f"Channel '{channel}' not found in the .nhf file. Available channels: {available_channels}")

        # Load image
        image_data = group[dataset_name][()]
        im = np.reshape(image_data, (x_pixel, y_pixel)).T

        # Image attributes
        s['channel'] = attrs['name']
        cali_min = attrs['base_calibration_min']
        cali_max = attrs['base_calibration_max']
        s['channel_units'] = attrs['base_calibration_unit']
        Bit = 2**31
        cali_factor = (cali_max - cali_min) / (Bit * 2.0)
        im = (im + Bit) * cali_factor + cali_min
        im = np.flip(im, axis=0)

        s['channels'] = [attrs.get('name')]

        im = np.rot90(im, k=1, axes=(0, 1))
        im = np.fliplr(im)

        # Extract required values
        num_frames = 1  # Assuming single frame for NHF
        x_range_nm = scan_size * 1e9
        y_pixels = y_pixel
        x_pixels = x_pixel
        fps = 1 / frame_acq_time if frame_acq_time != 0 else 0
        line_rate = y_pixel * fps if y_pixel else 0
        pixel_to_nanometre_scaling_factor = 1e9 / x_pixel  # Assuming equal scaling in x and y

        values = [
            str(num_frames),
            str(x_range_nm),
            f"{int(fps)}",
            f"{int(line_rate)}",
            str(y_pixels),
            str(x_pixels),
            f"{pixel_to_nanometre_scaling_factor:.2f}",
            channel
        ]

    return im, values, available_channels

if __name__ == "__main__":
    file_path = 'data/SBS-PS_example_data.nhf'
    channel = 'Topography'  # Replace with the appropriate channel name
    try:
        image, metadata, values = open_nhf(file_path, channel)
        print(f"Metadata: {metadata}")
        print(f"Image shape: {image.shape}")
        print(f"Parameter values: {values}")

        # Display the image using matplotlib
        import matplotlib.pyplot as plt
        plt.imshow(image, cmap=AFM)
        plt.colorbar(label=metadata['channel_units'])
        plt.show()
    except Exception as e:
        print(f"Error: {e}")
