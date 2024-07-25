import numpy as np

# Load the CSV file into a NumPy array
array = np.loadtxt('Rainbow.csv', delimiter=',').astype(np.float32)
print(array)

# Save the array to a .npy file
np.save('Rainbow.npy', array)
