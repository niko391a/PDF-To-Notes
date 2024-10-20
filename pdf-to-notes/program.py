import fitz  # PyMuPDF
import io
from PIL import Image
import os

def is_solid_color(image):
    # Get the pixel data of the image
    pixels = list(image.getdata())
    
    # Get the first pixel value to compare with the rest
    first_pixel = pixels[0]
    
    # Check if all pixels are the same as the first pixel
    return all(pixel == first_pixel for pixel in pixels)

def extract_images_from_pdf(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through the pages of the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        images = page.get_images(full=True)
        
        # Extract images from the page
        for image_index, img in enumerate(images):
            xref = img[0]  # xref is a unique reference for each image in the PDF
            base_image = pdf_document.extract_image(xref)
            if (len(base_image["image"]) / 1024) > 10 or not is_solid_color:
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
            
                # Save image to the output folder with a unique name
                image_output_path = f"{output_folder}/page_{page_number+1}_image_{image_index+1}.{image_ext}"
                image.save(image_output_path)
                print(f"Saved image: {image_output_path}")
    
    # Close the PDF
    pdf_document.close()
    print("Image extraction complete!")

# Example usage
pdf_path = "C:\\Users\\Nikol\\Downloads\\lecture 7.pdf"
output_folder = "C:\\Users\\Nikol\\Downloads\\lecture7-filtered"
extract_images_from_pdf(pdf_path, output_folder)