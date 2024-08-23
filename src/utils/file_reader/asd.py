from __future__ import annotations
from pathlib import Path
from typing import BinaryIO
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from matplotlib import animation
from utils.constants import STANDARDISED_METADATA_DICT_KEYS

from AFMReader.logging import logger
from AFMReader.io import (
    read_int32,
    read_int16,
    read_float,
    read_bool,
    read_hex_u32,
    read_ascii,
    read_uint8,
    read_null_separated_utf8,
    read_int8,
    read_double,
    skip_bytes,
)

logger.enable(__package__)

def calculate_scaling_factor(
    channel: str,
    z_piezo_gain: float,
    z_piezo_extension: float,
    scanner_sensitivity: float,
    phase_sensitivity: float,
) -> float:
    """
    Calculate the correct scaling factor.

    This function should be used in conjunction with the VoltageLevelConverter class to define the correct function and
    enables conversion between arbitrary level values from the AFM into real world nanometre height values.

    Parameters
    ----------
    channel : str
        The .asd channel being used.
    z_piezo_gain : float
        The z_piezo_gain listed in the header metadata for the .asd file.
    z_piezo_extension : float
        The z_piezo_extension listed in the header metadata for the .asd file.
    scanner_sensitivity : float
        The scanner_sensitivity listed in the header metadata for the .asd file.
    phase_sensitivity : float
        The phase_sensitivity listed in the heder metadata for the .asd file.

    Returns
    -------
    float
        The appropriate scaling factor to pass to a VoltageLevelConverter to convert arbitrary
        height levels to real world nanometre heights for the frame data in the specified channl
        in the .asd file.
    """
    if channel == "TP":
        return z_piezo_gain * z_piezo_extension
    if channel == "ER":
        return -scanner_sensitivity
    if channel == "PH":
        return -phase_sensitivity

    raise ValueError(f"channel {channel} not known for .asd file type.")


def load_asd(file_path: Path, channel: str):
    """
    Load a .asd file.

    Parameters
    ----------
    file_path : Path
        Path to the .asd file.
    channel : str
        Channel to load. Note that only three channels seem to be present in a single .asd file. Options: TP
        (Topograph), ER (Error) and PH (Phase).

    Returns
    -------
    npt.NDArray
        The .asd file frames data as a numpy 3D array N x W x H
        (Number of frames x Width of each frame x height of each frame).
    float
        The number of nanometres per pixel for the .asd file. (AKA the resolution).
        Enables converting between pixels and nanometres when working with the data, in order to use real-world length
        scales.
    dict
        Metadata for the .asd file. The number of entries is too long to list here, and changes based on the file
        version please either look into the `read_header_file_version_x` functions or print the keys too see what
        metadata is available.
    """
    # Ensure the file path is a Path object
    file_path = Path(file_path)
    # Open the file in binary mode
    with Path.open(file_path, "rb", encoding=None) as open_file:  # pylint: disable=unspecified-encoding
        file_version = read_file_version(open_file)

        if file_version == 0:
            header_dict = read_header_file_version_0(open_file)

        elif file_version == 1:
            header_dict = read_header_file_version_1(open_file)

        elif file_version == 2:
            header_dict = read_header_file_version_2(open_file)
        else:
            raise ValueError(
                f"File version {file_version} unknown. Please add support if you "
                "know how to decode this file version."
            )

        pixel_to_nanometre_scaling_factor_x = header_dict["x_pixels"] / header_dict["x_nm"]
        pixel_to_nanometre_scaling_factor_y = header_dict["y_pixels"] / header_dict["y_nm"]
        if pixel_to_nanometre_scaling_factor_x != pixel_to_nanometre_scaling_factor_y:
            logger.warning(
                f"Resolution of image is different in x and y directions:"
                f"x: {pixel_to_nanometre_scaling_factor_x}"
                f"y: {pixel_to_nanometre_scaling_factor_y}"
            )
        pixel_to_nanometre_scaling_factor = pixel_to_nanometre_scaling_factor_x

        if channel == header_dict["channel1"]:
            logger.info(f"Requested channel {channel} matches first channel in file: {header_dict['channel1']}")
        elif channel == header_dict["channel2"]:
            # Skip first channel data
            _size_of_frame_header = header_dict["frame_header_length"]
            # Remember that each value is two bytes (since signed int16)
            size_of_single_frame_plus_header = (
                header_dict["frame_header_length"] + header_dict["x_pixels"] * header_dict["y_pixels"] * 2
            )
            length_of_all_first_channel_frames = header_dict["num_frames"] * size_of_single_frame_plus_header
            _ = open_file.read(length_of_all_first_channel_frames)
        else:
            channel = header_dict["channel1"]

        scaling_factor = calculate_scaling_factor(
            channel=channel,
            z_piezo_gain=header_dict["z_piezo_gain"],
            z_piezo_extension=header_dict["z_piezo_extension"],
            scanner_sensitivity=header_dict["scanner_sensitivity"],
            phase_sensitivity=header_dict["phase_sensitivity"],
        )

        frames, frame_metadata_list = read_channel_data(
            open_file=open_file,
            num_frames=header_dict["num_frames"],
            x_pixels=header_dict["x_pixels"],
            y_pixels=header_dict["y_pixels"],
            frame_time=header_dict["frame_time"]
        )

        frames = np.array(frames)

        # Ensure channels are returned
        channels = [header_dict["channel1"], header_dict["channel2"]]

        # Ensure metadata includes channels
        header_dict["channels"] = channels

        fps = 1000.0 / header_dict.get('frame_time', 1000.0)  # Default to 1 fps if frame_time is missing
        line_rate = header_dict.get('y_pixels', 1) / (header_dict.get('frame_time', 1000.0) / 1000.0)
        values = [
            header_dict.get('num_frames', 'N/A'),
            [header_dict.get('x_nm', 'N/A') for i in range(header_dict.get('num_frames', 0))],
            fps,
            line_rate,
            header_dict.get('y_pixels', 'N/A'),
            header_dict.get('x_pixels', 'N/A'),
            [pixel_to_nanometre_scaling_factor for i in range(header_dict.get('num_frames', 'N/A'))],
            channel,
            [frame_metadata_list[i]["timestamp"] for i in range(int(header_dict.get('num_frames', 'N/A')))]
        ]

        if len(values) != len(STANDARDISED_METADATA_DICT_KEYS):
            raise ValueError(f"The length of the values in .asd does not match the required metadata keys.")

        # Create the metadata dictionary
        file_metadata = dict(zip(STANDARDISED_METADATA_DICT_KEYS, values))

        return frames, file_metadata, channels


def read_file_version(open_file: BinaryIO) -> int:
    """
    Read the file version from an open asd file. File versions are 0, 1 and 2.

    Different file versions require different functions to read the headers as the formatting changes between them.

    Parameters
    ----------
    open_file : BinaryIO
        An open binary file object for a .asd file.

    Returns
    -------
    int
        Integer file version decoded from file.
    """
    file_version = read_int32(open_file)
    return file_version


def read_header_file_version_0(open_file: BinaryIO) -> dict:
    """
    Read the header metadata for a .asd file using file version 0.

    Parameters
    ----------
    open_file : BinaryIO
        An open binary file object for a .asd file.

    Returns
    -------
    dict
        Dictionary of metadata decoded from the file header.
    """
    header_dict = {}
    header_dict["channel1"] = read_ascii(open_file, 2)
    header_dict["channel2"] = read_ascii(open_file, 2)
    header_dict["header_length"] = read_int32(open_file)
    header_dict["frame_header_length"] = read_int32(open_file)
    header_dict["user_name_size"] = read_int32(open_file)
    header_dict["comment_offset_size"] = read_int32(open_file)
    header_dict["comment_size"] = read_int32(open_file)
    header_dict["x_pixels"] = read_int16(open_file)
    header_dict["y_pixels"] = read_int16(open_file)
    header_dict["x_nm"] = read_int16(open_file)
    header_dict["y_nm"] = read_int16(open_file)
    header_dict["frame_time"] = read_float(open_file)
    header_dict["z_piezo_extension"] = read_float(open_file)
    header_dict["z_piezo_gain"] = read_float(open_file)
    header_dict["analogue_digital_range"] = read_hex_u32(open_file)
    header_dict["analogue_digital_data_bits_size"] = read_int32(open_file)
    header_dict["analogue_digital_resolution"] = 2 ^ header_dict["analogue_digital_data_bits_size"]
    header_dict["is_averaged"] = read_bool(open_file)
    header_dict["averaging_window"] = read_int32(open_file)
    _ = read_int16(open_file)
    header_dict["year"] = read_int16(open_file)
    header_dict["month"] = read_uint8(open_file)
    header_dict["day"] = read_uint8(open_file)
    header_dict["hour"] = read_uint8(open_file)
    header_dict["minute"] = read_uint8(open_file)
    header_dict["second"] = read_uint8(open_file)
    header_dict["rounding_degree"] = read_uint8(open_file)
    header_dict["max_x_scan_range"] = read_float(open_file)
    header_dict["max_y_scan_range"] = read_float(open_file)
    _ = read_int32(open_file)
    _ = read_int32(open_file)
    _ = read_int32(open_file)
    header_dict["initial_frames"] = read_int32(open_file)
    header_dict["num_frames"] = read_int32(open_file)
    header_dict["afm_id"] = read_int32(open_file)
    header_dict["file_id"] = read_int16(open_file)
    header_dict["user_name"] = read_null_separated_utf8(open_file, length_bytes=header_dict["user_name_size"])
    header_dict["scanner_sensitivity"] = read_float(open_file)
    header_dict["phase_sensitivity"] = read_float(open_file)
    header_dict["scan_direction"] = read_int32(open_file)
    _ = skip_bytes(open_file, header_dict["comment_offset_size"])
    comment = []
    for _ in range(header_dict["comment_size"]):
        comment.append(chr(read_int8(open_file)))
    header_dict["comment_without_null"] = "".join([c for c in comment if c != "\x00"])

    return header_dict


def read_header_file_version_1(open_file: BinaryIO) -> dict:
    """
    Read the header metadata for a .asd file using file version 1.

    Parameters
    ----------
    open_file : BinaryIO
        An open binary file object for a .asd file.

    Returns
    -------
    dict
        Dictionary of metadata decoded from the file header.
    """
    header_dict = {}
    header_dict["header_length"] = read_int32(open_file)
    header_dict["frame_header_length"] = read_int32(open_file)
    header_dict["text_encoding"] = read_int32(open_file)
    header_dict["user_name_size"] = read_int32(open_file)
    header_dict["comment_size"] = read_int32(open_file)
    header_dict["channel1"] = read_null_separated_utf8(open_file, length_bytes=4)
    header_dict["channel2"] = read_null_separated_utf8(open_file, length_bytes=4)
    header_dict["initial_frames"] = read_int32(open_file)
    header_dict["num_frames"] = read_int32(open_file)
    header_dict["scan_direction"] = read_int32(open_file)
    header_dict["file_id"] = read_int32(open_file)
    header_dict["x_pixels"] = read_int32(open_file)
    header_dict["y_pixels"] = read_int32(open_file)
    header_dict["x_nm"] = read_int32(open_file)
    header_dict["y_nm"] = read_int32(open_file)
    header_dict["is_averaged"] = read_bool(open_file)
    header_dict["averaging_window"] = read_int32(open_file)
    header_dict["year"] = read_int32(open_file)
    header_dict["month"] = read_int32(open_file)
    header_dict["day"] = read_int32(open_file)
    header_dict["hour"] = read_int32(open_file)
    header_dict["minute"] = read_int32(open_file)
    header_dict["second"] = read_int32(open_file)
    header_dict["x_rounding_degree"] = read_int32(open_file)
    header_dict["y_rounding_degree"] = read_int32(open_file)
    header_dict["frame_time"] = read_float(open_file)
    header_dict["scanner_sensitivity"] = read_float(open_file)
    header_dict["phase_sensitivity"] = read_float(open_file)
    header_dict["offset"] = read_int32(open_file)
    _ = skip_bytes(open_file, 12)
    header_dict["afm_id"] = read_int32(open_file)
    header_dict["analogue_digital_range"] = read_hex_u32(open_file)
    header_dict["analogue_digital_data_bits_size"] = read_int32(open_file)
    header_dict["analogue_digital_resolution"] = 2 ^ header_dict["analogue_digital_data_bits_size"]
    header_dict["max_x_scan_range"] = read_float(open_file)
    header_dict["max_y_scan_range"] = read_float(open_file)
    header_dict["x_piezo_extension"] = read_float(open_file)
    header_dict["y_piezo_extension"] = read_float(open_file)
    header_dict["z_piezo_extension"] = read_float(open_file)
    header_dict["z_piezo_gain"] = read_float(open_file)

    user_name = []
    for _ in range(header_dict["user_name_size"]):
        user_name.append(chr(read_int8(open_file)))
    header_dict["user_name"] = "".join([c for c in user_name if c != "\x00"])

    comment = []
    for _ in range(header_dict["comment_size"]):
        comment.append(chr(read_int8(open_file)))
    header_dict["comment_without_null"] = "".join([c for c in comment if c != "\x00"])

    return header_dict


def read_header_file_version_2(open_file: BinaryIO) -> dict:
    """
    Read the header metadata for a .asd file using file version 2.

    Parameters
    ----------
    open_file : BinaryIO
        An open binary file object for a .asd file.

    Returns
    -------
    dict
        Dictionary of metadata decoded from the file header.
    """
    header_dict = {}
    header_dict["header_length"] = read_int32(open_file)
    header_dict["frame_header_length"] = read_int32(open_file)
    header_dict["text_encoding"] = read_int32(open_file)
    header_dict["user_name_size"] = read_int32(open_file)
    header_dict["comment_size"] = read_int32(open_file)
    header_dict["channel1"] = read_null_separated_utf8(open_file, length_bytes=4)
    header_dict["channel2"] = read_null_separated_utf8(open_file, length_bytes=4)
    header_dict["initial_frames"] = read_int32(open_file)
    header_dict["num_frames"] = read_int32(open_file)
    header_dict["scan_direction"] = read_int32(open_file)
    header_dict["file_id"] = read_int32(open_file)
    header_dict["x_pixels"] = read_int32(open_file)
    header_dict["y_pixels"] = read_int32(open_file)
    header_dict["x_nm"] = read_int32(open_file)
    header_dict["y_nm"] = read_int32(open_file)
    header_dict["is_averaged"] = read_bool(open_file)
    header_dict["averaging_window"] = read_int32(open_file)
    header_dict["year"] = read_int32(open_file)
    header_dict["month"] = read_int32(open_file)
    header_dict["day"] = read_int32(open_file)
    header_dict["hour"] = read_int32(open_file)
    header_dict["minute"] = read_int32(open_file)
    header_dict["second"] = read_int32(open_file)
    header_dict["x_rounding_degree"] = read_int32(open_file)
    header_dict["y_rounding_degree"] = read_int32(open_file)
    header_dict["frame_time"] = read_float(open_file)
    header_dict["scanner_sensitivity"] = read_float(open_file)
    header_dict["phase_sensitivity"] = read_float(open_file)
    header_dict["offset"] = read_int32(open_file)
    _ = skip_bytes(open_file, 12)
    header_dict["afm_id"] = read_int32(open_file)
    header_dict["analogue_digital_range"] = read_hex_u32(open_file)
    header_dict["analogue_digital_data_bits_size"] = read_int32(open_file)
    header_dict["analogue_digital_resolution"] = 2 ^ header_dict["analogue_digital_data_bits_size"]
    header_dict["max_x_scan_range"] = read_float(open_file)
    header_dict["max_y_scan_range"] = read_float(open_file)
    header_dict["x_piezo_extension"] = read_float(open_file)
    header_dict["y_piezo_extension"] = read_float(open_file)
    header_dict["z_piezo_extension"] = read_float(open_file)
    header_dict["z_piezo_gain"] = read_float(open_file)

    user_name = []
    for _ in range(header_dict["user_name_size"]):
        user_name.append(chr(read_int8(open_file)))
    header_dict["user_name"] = "".join([c for c in user_name if c != "\x00"])

    comment = []
    for _ in range(header_dict["comment_size"]):
        comment.append(chr(read_int8(open_file)))
    header_dict["comment_without_null"] = "".join([c for c in comment if c != "\x00"])

    header_dict["number_of_frames"] = read_int32(open_file)
    header_dict["is_x_feed_forward_integer"] = read_int32(open_file)
    header_dict["is_x_feed_forward_double"] = read_double(open_file)
    header_dict["max_colour_scale"] = read_int32(open_file)
    header_dict["min_colour_scale"] = read_int32(open_file)
    header_dict["length_red_anchor_points"] = read_int32(open_file)
    header_dict["length_green_anchor_points"] = read_int32(open_file)
    header_dict["length_blue_anchor_points"] = read_int32(open_file)

    coords_red = []
    for _ in range(header_dict["length_red_anchor_points"]):
        anchor_x = read_int32(open_file)
        anchor_y = read_int32(open_file)
        coords_red.append((anchor_x, anchor_y))
    coords_green = []
    for _ in range(header_dict["length_green_anchor_points"]):
        anchor_x = read_int32(open_file)
        anchor_y = read_int32(open_file)
        coords_green.append((anchor_x, anchor_y))
    coords_blue = []
    for _ in range(header_dict["length_blue_anchor_points"]):
        anchor_x = read_int32(open_file)
        anchor_y = read_int32(open_file)
        coords_blue.append((anchor_x, anchor_y))

    return header_dict


def read_channel_data(
    open_file: BinaryIO,
    num_frames: int,
    x_pixels: int,
    y_pixels: int,
    frame_time: float
) -> tuple[npt.NDArray, list]:
    """
    Read frame data from an open .asd file, starting at the current position.

    Parameters
    ----------
    open_file : BinaryIO
        An open binary file object for a .asd file.
    num_frames : int
        The number of frames for this set of frame data.
    x_pixels : int
        The width of each frame in pixels.
    y_pixels : int
        The height of each frame in pixels.
    frame_time : float
        The time per frame in milliseconds.

    Returns
    -------
    tuple[np.ndarray, list]
        The extracted frame heightmap data as a N x W x H 3D numpy array
        (number of frames x width of each frame x height of each frame) and
        a list of frame-specific metadata dictionaries.
    """
    frames = []
    frame_metadata_list = []

    for i in range(num_frames):
        frame_header_dict = {}
        frame_header_dict["frame_number"] = read_int32(open_file)
        frame_header_dict["max_data"] = read_int16(open_file)
        frame_header_dict["min_data"] = read_int16(open_file)
        frame_header_dict["x_offset"] = read_int16(open_file)
        frame_header_dict["y_offset"] = read_int16(open_file)
        frame_header_dict["x_tilt"] = read_float(open_file)
        frame_header_dict["y_tilt"] = read_float(open_file)
        frame_header_dict["is_stimulated"] = read_bool(open_file)
        _booked_1 = read_int8(open_file)
        _booked_2 = read_int16(open_file)
        _booked_3 = read_int32(open_file)
        _booked_4 = read_int32(open_file)

        frame_header_dict["total_size"] = x_pixels * y_pixels
        frame_header_dict["total_byte_size"] = frame_header_dict["total_size"] * 2
        frame_data = open_file.read(frame_header_dict["total_size"] * 2)
        frame_data = np.frombuffer(frame_data, dtype=np.int16)
        frame_data = frame_data.reshape((y_pixels, x_pixels))

        # Multiply the frame data by -1 to adjust the display
        frame_data = frame_data * -1

        frames.append(frame_data)

        # Add the frame-specific metadata to the list
        frame_metadata_list.append({
            # 'frame_index': i,
            # 'max_data': frame_header_dict["max_data"],
            # 'min_data': frame_header_dict["min_data"],
            # 'x_offset': frame_header_dict["x_offset"],
            # 'y_offset': frame_header_dict["y_offset"],
            # 'x_tilt': frame_header_dict["x_tilt"],
            # 'y_tilt': frame_header_dict["y_tilt"],
            # 'is_stimulated': frame_header_dict["is_stimulated"],
            'timestamp': i * frame_time / 1000.0  # Calculate timestamp in seconds
        })

    return frames, frame_metadata_list

def create_animation(frames: npt.NDArray) -> None:
    """
    Create animation from a numpy array of frames (2d numpy arrays).

    File format can be specified, defaults to .gif.

    Parameters
    ----------
    file_name : str
        Name of the file to save.
    frames : npt.NDArray
        Numpy array of frames of shape (N x W x H) where N is the number of frames,
        W is the width of the frames and H is the height of the frames.
    file_format : str
        Optional string for the file format to save as. Formats currently available: .mp4, .gif.
    """
    fig, axis = plt.subplots()

    def update(frame: npt.NDArray):
        """
        Update the image with the latest frame.

        Parameters
        ----------
        frame : npt.NDArray
            Single frame to add to the image.

        Returns
        -------
        axis
            Matplotlib axis.
        """
        axis.imshow(frames[frame], cmap='gray')
        return axis

    # Create the animation object
    ani = animation.FuncAnimation(fig, update, frames=frames.shape[0], interval=200)

    plt.show()
