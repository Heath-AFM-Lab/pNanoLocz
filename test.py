from collections import Counter

channels = [
    ['height_retrace', 'measuredHeight_trace', 'height_trace'],
    ['height_retrace', 'height_trace']
]

print("Initial channels:", channels)
repeating_channels = []
for frame_number, frame_channels in enumerate(channels):
    if frame_number == 0:
        repeating_channels = frame_channels
        continue

    # Counter of the current repeating_channels
    counter1 = Counter(repeating_channels)
    # Counter of the current frame_channels
    counter2 = Counter(frame_channels)
    
    # Intersection with counts
    common_counter = counter1 & counter2
    
    # Convert the common elements counter to a list
    repeating_channels = list(common_counter.elements())

print("Repeating channels:", repeating_channels)