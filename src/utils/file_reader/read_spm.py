from __future__ import annotations
from pathlib import Path
import pySPM
import numpy as np
import logging
import matplotlib.colors as colors

AFM = np.load('utils/file_reader/AFM_cmap.npy')
AFM = colors.ListedColormap(AFM)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def spm_pixel_to_nm_scaling(filename: str, channel_data: pySPM.SPM.SPM_image) -> float:
    """
    Extract pixel to nm scaling from the SPM image metadata.

    Parameters
    ----------
    filename : str
        File name.
    channel_data : pySPM.SPM.SPM_image
        Channel data from PySPM.

    Returns
    -------
    float
        Pixel to nm scaling factor.
    """
    unit_dict = {
        "nm": 1,
        "um": 1e3,
    }
    px_to_real = channel_data.pxs()
    pixel_to_nm_scaling = (
        px_to_real[0][0] * unit_dict.get(px_to_real[0][1], 1),
        px_to_real[1][0] * unit_dict.get(px_to_real[1][1], 1),
    )[0]
    if px_to_real[0][0] == 0 and px_to_real[1][0] == 0:
        pixel_to_nm_scaling = 1
        logger.info(f"[{filename}] : Pixel size not found in metadata, defaulting to 1nm")
    logger.info(f"[{filename}] : Pixel to nm scaling : {pixel_to_nm_scaling}")
    return pixel_to_nm_scaling

def open_spm(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict, list]:
    """
    Extract image and pixel to nm scaling from the Bruker .spm file.

    Parameters
    ----------
    file_path : Path or str
        Path to the .spm file.
    channel : str
        Channel name to extract from the .spm file.

    Returns
    -------
    tuple[np.ndarray, dict, list]
        A tuple containing the image, its metadata including pixel to nanometre scaling value, and parameter values.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    ValueError
        If the channel is not found in the .spm file.
    """
    logger.info(f"Loading image from : {file_path}")
    file_path = Path(file_path)
    filename = file_path.stem
    try:
        scan = pySPM.Bruker(file_path)
        logger.info(f"[{filename}] : Loaded image from : {file_path}")

        labels = []
        for layer in scan.layers:
            for data in layer.get(b"@2:Image Data", []):
                raw_channel_name = data.decode("latin1", errors="ignore")
                channel_name = raw_channel_name.split('"')[1] if '"' in raw_channel_name else raw_channel_name
                labels.append(channel_name)

        if channel not in labels:
            logger.warning(f"[{filename}] : Channel '{channel}' not found. Using first available channel: {labels[0]}")
            channel = labels[0]

        channel_data = scan.get_channel(channel)
        logger.info(f"[{filename}] : Extracted channel {channel}")
        image = np.flipud(np.array(channel_data.pixels))
    except FileNotFoundError:
        logger.error(f"[{filename}] File not found : {file_path}")
        raise
    except Exception as e:
        if "Channel" in str(e) and "not found" in str(e):
            logger.error(f"[{filename}] : {channel} not in {file_path.suffix} channel list: {labels}")
            raise ValueError(f"{channel} not in {file_path.suffix} channel list: {labels}") from e
        raise e

    scaling_factor = spm_pixel_to_nm_scaling(filename, channel_data)
    metadata = {
        'scaling_factor': scaling_factor,
        'channel': channel,
        'channels': labels
    }

    # Extract required values
    num_frames = 1  # Assuming single frame for SPM
    y_pixels, x_pixels = image.shape
    x_range_nm = x_pixels * scaling_factor

    # Attempt to extract the scan rate from available metadata
    scan_rate = 0
    for layer in scan.layers:
        for key, value in layer.items():
            key_str = key.decode("latin1", errors="ignore") if isinstance(key, bytes) else key
            if 'Scan Rate' in key_str:
                scan_rate = float(value)
                break

    fps = 1 / scan_rate if scan_rate != 0 else 0
    line_rate = y_pixels * fps if y_pixels else 0
    pixel_to_nanometre_scaling_factor = scaling_factor

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

    return image, values, labels

if __name__ == "__main__":
    file_path = 'data/0.0_00014.spm'
    channel = 'None'  # Replace with the appropriate channel name
    try:
        image, values, labels = open_spm(file_path, channel)
        print(f"Parameter values: {values}")
        print(labels)

        # Display the image using matplotlib
        import matplotlib.pyplot as plt
        plt.imshow(image, cmap=AFM)
        plt.colorbar(label='Height (nm)')
        plt.show()
    except Exception as e:
        print(f"Error: {e}")
