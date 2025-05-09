# CubeSat Image DCT Compression Pipeline

## Overview  
This repository contains two Python scripts that implement a full-frame Discrete Cosine Transform (DCT) encoding/decoding pipeline for 64×64 RGB images captured by an ESP32-CAM (OV2640) aboard our CubeSat. Because our satellite uses low-bandwidth LoRa radio for downlink, we perform DCT compression onboard to reduce the data volume before transmission.

## Hardware & Communications  
- **Camera:** OV2640 module on ESP32-CAM  
- **Onboard Processor:** ESP32 microcontroller  
- **Downlink Radio:** LoRa (Long Range) transceiver  
- **Ground Station:** Python environment with SciPy, NumPy, Pillow, and Matplotlib  

## Why DCT?  
- **Energy compaction:** DCT concentrates most of an image’s visual information into a small number of low-frequency coefficients.  
- **Bandwidth savings:** By rounding and transmitting only the most significant coefficients (or the full 64×64 block when necessary), we dramatically shrink the data payload for LoRa downlinks.  
- **Simplicity:** Full-frame 64×64 DCT requires only two 1-D DCT calls per axis (via SciPy), making it computationally feasible on the ESP32.

## Repository Contents  
- `generate_dct_data.py`  
  - Loads a 64×64 RGB image (from file or camera capture)  
  - Computes a full-frame 2-D DCT on each color channel  
  - Rounds coefficients to integers and writes them to `dct_data.txt` in the format:  
    ```
    DCT_R = "c0,c1,…,c4095"
    DCT_G = "c0,c1,…,c4095"
    DCT_B = "c0,c1,…,c4095"
    ```
- `decode_and_display_rgb_dct.py`  
  - Reads `dct_data.txt`  
  - Strips labels/quotes and parses the 4096 coefficients per channel  
  - Performs the inverse DCT (IDCT) to reconstruct the 64×64 RGB image  
  - Displays the result with Matplotlib and saves it as `reconstructed.png`

## Usage

1. **Encoding (Ground or Onboard):**  
   ```bash
   python generate_dct_data.py path/to/your_image.png
