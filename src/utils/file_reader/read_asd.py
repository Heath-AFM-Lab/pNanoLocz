import numpy as np
from pathlib import Path
from asd import load_asd, create_animation  



def main(file_path: str, channel: str, shift: int = 207):
    # Load the .asd file
    frames, pixel_to_nanometre_scaling_factor, metadata = load_asd(file_path=Path(file_path), channel=channel)

    # Check the shape of the images
    print("Metadata: ", metadata)
    print("Pixel to Nanometre Scaling Factor", pixel_to_nanometre_scaling_factor)
    print("Image shape: ", frames.shape)

    create_animation("output", frames)

if __name__ == "__main__":
    file_path = 'data/070920180003.asd'
    channel = "TP"  # Set the channel to "TP", "ER", or "PH"
    main(file_path, channel)
