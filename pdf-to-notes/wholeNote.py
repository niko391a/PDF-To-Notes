import fitz  # PyMuPDF
import io
import os
from pdf2image import convert_from_path
from PIL import Image

# Main execution
pdf_path = "C:\\Users\\Nikol\\Downloads\\IDBS - Lecture 8.pdf"
output_folder = "C:\\Users\\Nikol\\Downloads\\IDBS - Lecture 8-filtered"
subfolder = "attachments-lecture8-IDBS"

def extract_images_from_pdf(pdf_path, output_folder):
    attachments_folder = os.path.join(output_folder, subfolder)
    
    # Create output folders if they don't exist
    os.makedirs(attachments_folder, exist_ok=True)

    pdf_document = fitz.open(pdf_path)
    
    # Iterate through the pages of the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        images = page.get_images(full=True)

        # Extract images from the page
        for image_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))

            # Save image to the attachments folder with a simple name
            image_output_path = f"{attachments_folder}/page_{page_number + 1}.{image_ext}"
            image.save(image_output_path)

    pdf_document.close()

def convert_pdf_to_images(pdf_path, output_folder):
    attachments_folder = os.path.join(output_folder, subfolder)
    
    # Create output folder for attachments if it doesn't exist
    os.makedirs(attachments_folder, exist_ok=True)

    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        image_path = f"{attachments_folder}/page_{i + 1}.png"  # Save as PNG for vector graphics
        page.save(image_path, 'PNG')

def extract_text_for_all_pages(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_data = {}
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        text = page.get_text("text")
        
        # Split text into lines
        lines = text.split('\n')
        page_text = ""

        for line in lines:
            page_text += line + "\n"

        text_data[page_number] = {
            "title": lines[0] if lines else f"Page {page_number + 1}",
            "content": page_text.strip()
        }

    pdf_document.close()
    return text_data

def create_markdown(pdf_path, output_folder):
    text_data = extract_text_for_all_pages(pdf_path)
    md_file_path = os.path.join(output_folder, "extracted_content.md")

    with open(md_file_path, "w", encoding="utf-8") as md_file:  # Set encoding to UTF-8
        for page_number, data in text_data.items():
            print(f"Processing page {page_number + 1}")  # Debug statement
            
            # Adding the title
            md_file.write(f"# {data['title']}\n\n")
            
            # Adding the corresponding image reference in Obsidian format
            image_file = f"page_{page_number + 1}"  # Image reference without extension
            md_file.write(f"![[{image_file}.png]]\n\n")
            
            # Adding the extracted text content
            md_file.write(f"{data['content']}\n\n")
            
            md_file.write("\n---\n\n")

    print("Markdown creation complete!")

# Create output folder for images and markdown
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Step 1: Extract images from PDF
extract_images_from_pdf(pdf_path, output_folder)

# Step 2: Convert PDF pages to images (for vector graphics)
convert_pdf_to_images(pdf_path, output_folder)

# Step 3: Create markdown file combining text and images
create_markdown(pdf_path, output_folder)

print("Extraction and markdown creation complete!")
