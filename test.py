import numpy as np

data = np.array([[1., 2, 3, 4, 5],
                [1,2,3,4,5],
                [1,2,3,4,5]
])

# Calculate the mean
mean = np.mean(data)
print("Mean:", mean)  # Mean: 3.0

# Calculate the standard deviation
std_dev = np.std(data)
print("Standard Deviation:", std_dev)  # Standard Deviation: 1.4142135623730951
