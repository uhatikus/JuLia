import os
from PIL import Image
from pathlib import Path

def create_mini_photos(input_folder="photos", output_folder="photos_mini", min_dimension=512):
    """
    Create mini versions of photos with minimum dimension of 256 pixels.
    
    Args:
        input_folder (str): Folder containing original photos
        output_folder (str): Folder to save mini photos
        min_dimension (int): Minimum dimension for the output images
    """
    
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(exist_ok=True)
    
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
    
    # Get all image files from input folder
    input_path = Path(input_folder)
    image_files = [f for f in input_path.iterdir() 
                  if f.is_file() and f.suffix.lower() in supported_formats]
    
    if not image_files:
        print(f"No supported image files found in '{input_folder}'")
        return
    
    print(f"Found {len(image_files)} image files to process")
    
    processed_count = 0
    error_count = 0
    
    for image_file in image_files:
        try:
            # Open the image
            with Image.open(image_file) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Calculate new dimensions while maintaining aspect ratio
                width, height = img.size
                
                if width < height:
                    # Portrait orientation
                    new_width = min_dimension
                    new_height = int(height * (min_dimension / width))
                else:
                    # Landscape orientation or square
                    new_height = min_dimension
                    new_width = int(width * (min_dimension / height))
                
                # Resize the image
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Create output filename
                output_filename = f"{image_file.stem}_mini{image_file.suffix}"
                output_path = Path(output_folder) / output_filename
                
                # Save the resized image with optimized quality
                if image_file.suffix.lower() in ['.jpg', '.jpeg']:
                    resized_img.save(output_path, 'JPEG', quality=85, optimize=True)
                elif image_file.suffix.lower() == '.png':
                    resized_img.save(output_path, 'PNG', optimize=True)
                else:
                    resized_img.save(output_path)
                
                processed_count += 1
                print(f"Processed: {image_file.name} -> {output_filename}")
                
        except Exception as e:
            error_count += 1
            print(f"Error processing {image_file.name}: {str(e)}")
    
    print("\nProcessing complete!")
    print(f"Successfully processed: {processed_count} files")
    print(f"Errors: {error_count} files")

if __name__ == "__main__":
    # Run the function
    create_mini_photos()