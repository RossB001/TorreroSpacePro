import sys
from PIL import Image
import numpy as np
from scipy.fftpack import dct

# --- 1. Load Image and ensure 64x64 RGB ---
if len(sys.argv) < 2:
    print("Usage: python script.py <input_image_path>")
    sys.exit(1)

image_path = sys.argv[1]
# Open the image using PIL
img = Image.open(image_path)
# Convert to RGB mode (in case the image is grayscale or palette)
img = img.convert('RGB')
# Resize to 64x64 if not already
if img.size != (64, 64):
    img = img.resize((64, 64))

# Convert the image to a NumPy array and split into R, G, B channels
img_array = np.array(img)
R = img_array[:, :, 0].astype(float)
G = img_array[:, :, 1].astype(float)
B = img_array[:, :, 2].astype(float)

# --- 2. Compute 2D DCT on each channel using SciPy ---
# Apply 1D DCT on columns (axis 0), then on rows (axis 1) for each channel
dct_R = dct(dct(R, axis=0, norm=None), axis=1, norm=None)
dct_G = dct(dct(G, axis=0, norm=None), axis=1, norm=None)
dct_B = dct(dct(B, axis=0, norm=None), axis=1, norm=None)

# --- 3. Round DCT coefficients to nearest integers ---
dct_R_int = np.rint(dct_R).astype(int)
dct_G_int = np.rint(dct_G).astype(int)
dct_B_int = np.rint(dct_B).astype(int)

# --- 4. Flatten and format output strings ---
flat_R = dct_R_int.flatten()
flat_G = dct_G_int.flatten()
flat_B = dct_B_int.flatten()

# Join coefficients into comma-separated strings
coeffs_R = ",".join(map(str, flat_R))
coeffs_G = ",".join(map(str, flat_G))
coeffs_B = ",".join(map(str, flat_B))

# Prepare the output lines with the exact required format
output_lines = [
    f'DCT_R = "{coeffs_R}"',
    f'DCT_G = "{coeffs_G}"',
    f'DCT_B = "{coeffs_B}"'
]

# Write the output to dct_data.txt (one line per channel)
with open("dct_data.txt", "w") as out_file:
    out_file.write("\n".join(output_lines))
