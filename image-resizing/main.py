import os
from PIL import Image

# Specify the input directory
input_directory = r'C:\Users\Muizz\Documents\vsCode\Resizing\leaf'

# Walk through the input directory and its subdirectories
for root, dirs, files in os.walk(input_directory):
    # Loop through all files in the current directory
    for filename in files:
        if filename.lower().endswith('.jpg'):
            img_path = os.path.join(root, filename)

            # Open the image
            with Image.open(img_path) as img:
                # Resize the image
                img = img.resize((256, 256))

                # Convert to RGB if the image has an alpha channel
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGB')

                # Save the resized image, replacing the original one
                img.save(img_path)

print("Resizing and replacing complete!")
