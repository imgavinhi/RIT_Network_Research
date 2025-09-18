import numpy as np
from feature_construction import num_rows, numpy_x_y, mean_normalization, fields_and_labels

# --- Configuration ---
# Match the 'features' value used in your main script
features = 16 
# Match the dimensions you chose for your CNN
packet_height = 4
packet_width = 4
# The path to your sample data file
test_file = 'test_data.txt'

# --- Step 1: Check rows and cols ---
print("Testing num_rows...")
x_rows, y_rows = num_rows(test_file)
print(f"Detected {x_rows} packets and {y_rows} labels.")
print("-" * 20)

# --- Step 2: Test 4D numpy array creation ---
print("Testing numpy_x_y...")
# Assume a mock y array for the purpose of this test
mock_y_cols = 1
x, y = numpy_x_y(x_rows, features, test_file, y_rows, mock_y_cols, packet_height, packet_width)
print(f"Created x array with shape: {x.shape}")
print("First packet data (before normalization):")
# The [0, 0, :, :] slices the first packet, first channel, and all rows/cols
print(x[0, 0, :, :])
print("-" * 20)

# --- Step 3: Test normalization ---
print("Testing mean_normalization_4d...")
x_normalized = mean_normalization_4d(x)
print(f"Normalized x array shape: {x_normalized.shape}")
print("First packet data (after normalization):")
print(x_normalized[0, 0, :, :])
print("-" * 20)

# --- Step 4: Test labeler (optional, but good practice) ---
# Note: You'll need to make a dummy y array with the correct shape for this to work
# or just skip this step if you're confident fields_and_labels works.
print("Testing fields_and_labels...")
# Assuming a mock y array of the correct shape is needed for this test
y_dummy = np.zeros((y_rows, 1)) 
y_labeled = fields_and_labels(test_file, y_dummy)
print(f"y_labeled array shape: {y_labeled.shape}")
print("First 5 labels:", y_labeled.flatten()[:5])
print("-" * 20)

print("All tests complete. Check the output for correctness.")
