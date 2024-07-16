from __future__ import annotations
from pathlib import Path
import numpy as np
from igor2 import binarywave
import matplotlib.pyplot as plt
import matplotlib.colors as colors

AFM = np.load('AFM_cmap.npy')
AFM = colors.ListedColormap(AFM)

def _ibw_pixel_to_nm_scaling(scan: dict) -> float:
    """
    Extract pixel to nm scaling from the IBW image metadata.

    Parameters
    ----------
    scan : dict
        The loaded binary wave object.

    Returns
    -------
    float
        A value corresponding to the real length of a single pixel.
    """
    notes = {}
    for line in str(scan["wave"]["note"]).split("\\r"):
        if ":" in line:
            key, val = line.split(":", 1)
            notes[key.strip()] = val.strip()
    return (
        float(notes["SlowScanSize"]) / scan["wave"]["wData"].shape[0] * 1e9,  # Convert to nm
        float(notes["FastScanSize"]) / scan["wave"]["wData"].shape[1] * 1e9,  # Convert to nm
    )[0]

def extract_metadata(notes: str) -> dict:
    """
    Extract metadata from the IBW notes.

    Parameters
    ----------
    notes : str
        The notes string from the IBW file.

    Returns
    -------
    dict
        A dictionary containing extracted metadata.
    """
    metadata = {}
    for line in notes.split("\\r"):
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    return metadata

def open_ibw(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict]:
    """
    Load image from Asylum Research (Igor) .ibw files.

    Parameters
    ----------
    file_path : Path | str
        Path to the .ibw file.
    channel : str
        The channel to extract from the .ibw file.

    Returns
    -------
    tuple[np.ndarray, dict]
        A tuple containing the image and metadata.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    ValueError
        If the channel is not found in the .ibw file.
    """
    file_path = Path(file_path)
    scan = binarywave.load(file_path)
    labels = []
    for label_list in scan["wave"]["labels"]:
        for label in label_list:
            if label:
                labels.append(label.decode())
    if channel not in labels:
        raise ValueError(f"Channel '{channel}' not found in {file_path}. Available channels: {labels}")
    
    channel_idx = labels.index(channel)
    image = scan["wave"]["wData"][:, :, channel_idx].T * 1e9  # Convert to nm
    image = np.flipud(image)
    scaling = _ibw_pixel_to_nm_scaling(scan)
    metadata = extract_metadata(str(scan["wave"]["note"]))
    metadata['scaling_factor'] = scaling

    return image, metadata

if __name__ == "__main__":
    file_path = 'data/tops70s14_190g0000.ibw'
    channel = 'HeightTracee'  # Replace with the appropriate channel name
    try:
        im, metadata = open_ibw(file_path, channel)
        print(f"Scaling factor: {metadata['scaling_factor']} nm/pixel")
        print(f"Image shape: {im.shape}")
        print("Metadata:", metadata)

        # Single frame case
        plt.imshow(im, cmap=AFM)
        plt.colorbar(label='Height (nm)')
        plt.show()

    except Exception as e:
        print(f"Error: {e}")
