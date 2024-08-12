import numpy as np
from pathlib import Path
import tifffile
from utils.constants import STANDARDISED_METADATA_DICT_KEYS

def _jpk_pixel_to_nm_scaling(tiff_page: tifffile.tifffile.TiffPage) -> float:
    length = tiff_page.tags["32834"].value  # Grid-uLength (fast)
    width = tiff_page.tags["32835"].value  # Grid-vLength (slow)
    length_px = tiff_page.tags["32838"].value  # Grid-iLength (fast)
    width_px = tiff_page.tags["32839"].value  # Grid-jLength (slow)
    px_to_nm = (length / length_px, width / width_px)[0]
    return 1/(px_to_nm * 1e9)

def extract_metadata(tiff_page: tifffile.tifffile.TiffPage) -> dict:
    metadata = {
        'x_Origin': tiff_page.tags.get("32832", np.nan).value,
        'y_Origin': tiff_page.tags.get("32833", np.nan).value,
        'x_scan_length': tiff_page.tags.get("32834", np.nan).value,
        'y_scan_length': tiff_page.tags.get("32835", np.nan).value,
        'x_scan_pixels': tiff_page.tags.get("32838", np.nan).value,
        'y_scan_pixels': tiff_page.tags.get("32839", np.nan).value,
        'Reference_Amp': tiff_page.tags.get("32821", np.nan).value,
        'Set_Amplitude': tiff_page.tags.get("32822", np.nan).value,
        'Oscillation_Freq': tiff_page.tags.get("32823", np.nan).value,
        'Scan_Rate': tiff_page.tags.get("32841", np.nan).value,  # Corrected to 'Scan_Rate'
    }
    return metadata

def open_jpk(file_path: Path | str, channel: str) -> tuple[np.ndarray, dict, list]:
    file_path = Path(file_path)
    with tifffile.TiffFile(file_path) as tif:
        channel_list = {}
        for i, page in enumerate(tif.pages[1:]):  # [0] is thumbnail
            available_channel = page.tags["32848"].value  # keys are hexadecimal values
            tr_rt = "trace" if page.tags["32849"].value == 0 else "retrace"
            channel_list[f"{available_channel}_{tr_rt}"] = i + 1
        
        if channel not in channel_list:
            channel = list(channel_list.keys())[0]

        channel_idx = channel_list[channel]
        channel_page = tif.pages[channel_idx]
        image = channel_page.asarray()
        scaling_type = channel_page.tags["33027"].value
        if scaling_type == "LinearScaling":
            scaling = channel_page.tags["33028"].value
            offset = channel_page.tags["33029"].value
            image = (image * scaling) + offset
        elif scaling_type != "NullScaling":
            raise ValueError(f"Scaling type {scaling_type} is not 'NullScaling' or 'LinearScaling'")

        metadata_page = tif.pages[0]
        metadata = extract_metadata(metadata_page)
        scaling_factor = _jpk_pixel_to_nm_scaling(metadata_page)
        metadata['scaling_factor'] = scaling_factor
        channels = list(channel_list.keys())

        # Rotate the image 90 degrees clockwise
        image_flipped = np.flipud(image) * 1e9

        # Extract required values
        num_frames = int(len(tif.pages[1:]) / len(channels))
        x_range_nm = float(metadata.get('x_scan_length', '0')) * 1e9
        y_pixels = int(metadata.get('y_scan_pixels', '0'))
        x_pixels = int(metadata.get('x_scan_pixels', '0'))
        scan_rate = float(metadata.get('Scan_Rate', '0'))
        scan_speed = scan_rate / y_pixels if y_pixels else 0
        fps = 1 / scan_speed if scan_speed != 0 else 0
        pixel_to_nanometre_scaling_factor = scaling_factor

        # Add calculated FPS to metadata
        metadata['fps'] = fps

        values = [
            num_frames,
            x_range_nm,
            fps,
            scan_rate,
            y_pixels,
            x_pixels,
            pixel_to_nanometre_scaling_factor,
            channel,
            None
        ]

        if len(values) != len(STANDARDISED_METADATA_DICT_KEYS):
            raise ValueError(f"The length of the values in .jpk does not match the required metadata keys.")

        # Create the metadata dictionary
        file_metadata = dict(zip(STANDARDISED_METADATA_DICT_KEYS, values))

    return image_flipped, file_metadata, channels

if __name__ == "__main__":
    file_path = 'data/save-2023.02.16-12.08.49.026.jpk'
    channel = 'height_trace'  # Replace with the appropriate channel name
    try:
        image, metadata, values = open_jpk(file_path, channel)
        print(f"Scaling factor: {metadata['scaling_factor']} nm/pixel")
        print(f"Image shape: {image.shape}")
        print("Metadata:", metadata)
        print(f"Parameter values: {values}")

        import matplotlib.pyplot as plt
        plt.imshow(image, cmap='gray')
        plt.colorbar(label='Height (nm)')
        plt.show()
    except Exception as e:
        print(f"Error: {e}")
