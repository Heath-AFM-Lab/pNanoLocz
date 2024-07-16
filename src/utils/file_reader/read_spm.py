from __future__ import annotations
from pathlib import Path
import pySPM
import numpy as np
import logging
import matplotlib.colors as colors

AFM = np.load('AFM_cmap.npy')
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

def open_spm(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict]:
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
    tuple[np.ndarray, dict]
        A tuple containing the image and its metadata including pixel to nanometre scaling value.

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
        channel_data = scan.get_channel(channel)
        logger.info(f"[{filename}] : Extracted channel {channel}")
        image = np.flipud(np.array(channel_data.pixels))
    except FileNotFoundError:
        logger.error(f"[{filename}] File not found : {file_path}")
        raise
    except Exception as e:
        if "Channel" in str(e) and "not found" in str(e):
            # Trying to return the error with options of possible channel values
            labels = []
            raw_labels = []
            for layer in scan.layers:
                for data in layer.get(b"@2:Image Data", []):
                    raw_channel_name = data.decode("latin1", errors="ignore")
                    raw_labels.append(raw_channel_name)
                    channel_name = raw_channel_name.split('"')[1][1:-1] if '"' in raw_channel_name else raw_channel_name
                    labels.append(channel_name)
            logger.error(f"[{filename}] : {channel} not in {file_path.suffix} channel list: {labels}")
            logger.error(f"Raw channel names: {raw_labels}")
            raise ValueError(f"{channel} not in {file_path.suffix} channel list: {labels}") from e
        raise e

    scaling_factor = spm_pixel_to_nm_scaling(filename, channel_data)
    metadata = {
        'scaling_factor': scaling_factor,
        'channel': channel,
    }

    return image, metadata

if __name__ == "__main__":
    file_path = 'data/0.0_00014.spm'
    channel = 'Height Sensor'  # Replace with the appropriate channel name
    try:
        image, metadata = open_spm(file_path, channel)
        print(f"Pixel to nm scaling: {metadata['scaling_factor']} nm/pixel")
        print(f"Image shape: {image.shape}")

        # Display the image using matplotlib
        import matplotlib.pyplot as plt
        plt.imshow(image, cmap=AFM)
        plt.colorbar(label='Height (nm)')
        plt.show()
    except Exception as e:
        print(f"Error: {e}")
