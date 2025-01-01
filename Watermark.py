from PIL import Image, ImageEnhance
import os

def apply_watermark(opacity=1.0, header_margin=20, header_top_margin=10):
    # Define directory paths
    wm_dir = 'WM'
    raw_dir = 'RAW'
    done_dir = 'Done'

    # Ensure the Done directory exists
    os.makedirs(done_dir, exist_ok=True)

    # Load the watermark image
    watermark_path = os.path.join(wm_dir, 'watermark.png')

    if not os.path.exists(watermark_path):
        print(f"Watermark image not found in {wm_dir}")
        return

    watermark = Image.open(watermark_path).convert("RGBA")
    watermark_width, watermark_height = watermark.size

    # Adjust watermark opacity
    if 0 <= opacity <= 1:
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    else:
        print("Opacity must be between 0 and 1. Using default opacity of 1.0.")

    # Process images in RAW directory
    for raw_image_name in os.listdir(raw_dir):
        raw_image_path = os.path.join(raw_dir, raw_image_name)

        if not os.path.isfile(raw_image_path):
            continue

        try:
            # Open the raw image
            raw_image = Image.open(raw_image_path).convert("RGBA")
            raw_width, raw_height = raw_image.size

            # Resize watermark to match the width of the raw image
            scale_factor = raw_width / watermark_width
            resized_wm_height = int(watermark_height * scale_factor)
            resized_watermark = watermark.resize((raw_width, resized_wm_height), Image.Resampling.LANCZOS)

            # Paste the watermark on the raw image
            # Calculate the watermark position
            watermark_x = (raw_width - resized_watermark.width) // 2  # Center horizontally
            watermark_y = (raw_height - resized_watermark.height) // 2  # Center vertically
            watermark_position = (watermark_x, watermark_y)

            raw_image.paste(resized_watermark, watermark_position, resized_watermark)

            # Save the final image
            final_image_path = os.path.join(done_dir, raw_image_name)
            raw_image.convert("RGB").save(final_image_path, "JPEG")
            print(f"Processed and moved: {raw_image_name}")

            # Remove the original image from RAW
            os.remove(raw_image_path)

        except Exception as e:
            print(f"Failed to process {raw_image_name}: {e}")

if __name__ == "__main__":
    # Example usage: Change opacity, header margin, and header top margin as needed
    apply_watermark(opacity=0.5, header_margin=30, header_top_margin=10)
