import fitz  # PyMuPDF

def is_solid_color(image):
    # Get the pixel data of the image
    pixels = list(image.getdata())
    
    # Get the first pixel value to compare with the rest
    first_pixel = pixels[0]
    
    # Check if all pixels are the same as the first pixel
    return all(pixel == first_pixel for pixel in pixels)

def inspect_images_in_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through the pages of the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        images = page.get_images(full=True)
        
        # Print information about each image on the page
        for image_index, img in enumerate(images):
            xref = img[0]  # xref is a unique reference for each image in the PDF
            base_image = pdf_document.extract_image(xref)
            if (len(base_image["image"]) / 1024) > 10 or not is_solid_color:
                print(f"Page {page_number+1}, Image {image_index+1}:")
                print(f" - xref: {xref}")
                print(f" - Width: {base_image['width']}")
                print(f" - Height: {base_image['height']}")
                print(f" - Colorspace: {base_image['colorspace']}")
                print(f" - File Type: {base_image['ext']}")
                print(f" - Image size: {len(base_image['image']) / 1024:.2f} KB")
                print("------")

    pdf_document.close()

# Example usage
pdf_path = "C:\\Users\\Nikol\\Downloads\\lecture6_logical_time.pdf"  # Replace with the path to your PDF file
inspect_images_in_pdf(pdf_path)
