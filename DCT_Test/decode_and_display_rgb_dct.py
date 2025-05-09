# decode_and_display_rgb_dct.py

import os, re
import numpy as np
from scipy.fftpack import idct
import matplotlib.pyplot as plt
from PIL import Image

def idct2(block):
    """2-D inverse DCT (Type-II↔Type-II with norm='ortho')."""
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def load_channel(line):
    """
    Given a line like DCT_R = "v1,v2,...", strip labels/quotes and
    return a 64×64 numpy array of ints.
    """
    # drop everything up to first quote
    if '"' in line:
        line = line.split('"', 1)[1]
    # drop trailing quote
    if line.endswith('"'):
        line = line[:-1]
    # remove whitespace
    line = re.sub(r'\s+', '', line)
    # parse ints
    coeffs = np.fromstring(line, sep=',', dtype=int)
    if coeffs.size != 64*64:
        raise ValueError(f"Expected 4096 coeffs, got {coeffs.size}")
    return coeffs.reshape((64,64))

def main():
    here = os.path.dirname(__file__)
    path = os.path.join(here, "dct_data.txt")
    if not os.path.exists(path):
        print("Error: dct_data.txt not found!")
        return

    # read exactly 3 lines
    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    if len(lines) < 3:
        raise RuntimeError("dct_data.txt must contain ≥3 non-empty lines")

    # load R, G, B
    dct_r = load_channel(lines[0])
    dct_g = load_channel(lines[1])
    dct_b = load_channel(lines[2])

    # inverse DCT
    img_r = idct2(dct_r)
    img_g = idct2(dct_g)
    img_b = idct2(dct_b)

    # stack and normalize to 0–255
    img = np.stack((img_r, img_g, img_b), axis=2)
    # scale so min→0, max→255
    mn, mx = img.min(), img.max()
    if mx > mn:
        img = (img - mn) / (mx - mn) * 255.0
    else:
        img = np.zeros_like(img)
    img = np.clip(img, 0, 255).astype(np.uint8)

    # display
    plt.figure(figsize=(4,4))
    plt.imshow(img)
    plt.axis("off")
    plt.title("Reconstructed Image from DCT")
    plt.show()

    # save
    out_path = os.path.join(here, "reconstructed.png")
    Image.fromarray(img).save(out_path)
    print(f"Saved reconstructed image to {out_path}")

if __name__ == "__main__":
    main()
