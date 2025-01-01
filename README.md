# Image Watermark Application Tool

## Overview
This Python script applies watermarks to images in bulk. It takes images from a `RAW` directory, applies a watermark from the `WM` directory, and saves the processed images in a `Done` directory. The watermark is automatically scaled to match the width of each image and positioned in the center.

## Features
- Bulk watermark processing
- Customizable watermark opacity
- Automatic watermark scaling
- Center positioning of watermark
- Automatic cleanup of processed raw images

## Prerequisites
- Python 3.x
- Pillow (PIL) library

To install required dependencies:
```bash
pip install Pillow
```

## Directory Structure
The script expects the following directory structure:
```
your_project_directory/
├── RAW/              # Place your original images here
├── WM/               # Contains watermark.png
│   └── watermark.png
└── Done/             # Processed images will be saved here
```

## Setup Instructions
1. Create the required directories:
   - `RAW` - for your original images
   - `WM` - for your watermark
   - `Done` - will be created automatically if it doesn't exist
2. Place your watermark image as `watermark.png` in the `WM` directory
3. Place all images to be watermarked in the `RAW` directory

## Usage
Basic usage with default settings:
```python
from watermark import apply_watermark

apply_watermark()
```

Customize opacity and margins:
```python
apply_watermark(
    opacity=0.5,        # 50% opacity
    header_margin=30,   # Horizontal margin
    header_top_margin=10  # Vertical margin from top
)
```

## Parameters
- `opacity` (float, default=1.0): Watermark opacity (0.0 to 1.0)
- `header_margin` (int, default=20): Horizontal margin in pixels
- `header_top_margin` (int, default=10): Top margin in pixels

## Process Flow
1. Script checks for required directories and watermark image
2. Each image in the `RAW` directory is processed:
   - Image is opened and converted to RGBA
   - Watermark is resized to match image width
   - Watermark is positioned in the center
   - Final image is saved as JPEG in the `Done` directory
   - Original image is removed from `RAW` directory
3. Processing status is printed for each image

## Error Handling
- Creates `Done` directory if it doesn't exist
- Skips non-file items in `RAW` directory
- Reports processing failures for individual images
- Validates opacity value range

## Notes
- Supports JPEG output format
- Processes images one at a time
- Automatically removes processed images from `RAW` directory
- Watermark is always centered on the image

## Limitations
- Requires watermark image to be named "watermark.png"
- Outputs only in JPEG format
- Cannot process images if watermark is missing
