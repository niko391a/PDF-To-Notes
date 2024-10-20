import fitz  # PyMuPDF
import io
import os
from pdf2image import convert_from_path
from PIL import Image

def extract_images_from_pdf(pdf_path, output_folder):
    attachments_folder = os.path.join(output_folder, "attachments")
    
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

            # Save image to the attachments folder with a unique name
            image_output_path = f"{attachments_folder}/page_{page_number+1}_image_{image_index+1}.{image_ext}"
            image.save(image_output_path)

    pdf_document.close()

def convert_pdf_to_images(pdf_path, output_folder):
    attachments_folder = os.path.join(output_folder, "attachments")
    
    # Create output folder for attachments if it doesn't exist
    os.makedirs(attachments_folder, exist_ok=True)

    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        image_path = f"{attachments_folder}/page_{i+1}.png"
        page.save(image_path, 'PNG')

def extract_text_and_bullet_points(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_data = {}
    
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        text = page.get_text("text")
        
        # Split text into lines
        lines = text.split('\n')
        page_text = ""
        bullet_points = []

        for line in lines:
            # Simple check for bullet points
            if line.startswith(('*', '-', '•', '–')):  # Add other bullet characters if needed
                bullet_points.append(line)
            else:
                page_text += line + "\n"

        text_data[page_number] = {
            "title": lines[0] if lines else f"Page {page_number + 1}",
            "content": page_text.strip(),
            "bullet_points": bullet_points
        }

    pdf_document.close()
    return text_data

def create_markdown(pdf_path, output_folder):
    text_data = extract_text_and_bullet_points(pdf_path)
    md_file_path = os.path.join(output_folder, "extracted_content.md")

    with open(md_file_path, "w") as md_file:
        for page_number, data in text_data.items():
            # Adding the title
            md_file.write(f"# {data['title']}\n\n")
            
            # Adding the corresponding image
            image_file = f"attachments/page_{page_number + 1}.png"  # Image corresponding to the page
            image_path = os.path.join(output_folder, image_file)
            md_file.write(f"![Image for {data['title']}]({image_path})\n\n")
            
            # Adding the extracted text content
            md_file.write(f"{data['content']}\n\n")
            
            # Adding bullet points if they exist
            if data['bullet_points']:
                md_file.write("## Bullet Points\n")
                for point in data['bullet_points']:
                    md_file.write(f"- {point}\n")
            md_file.write("\n---\n\n")

# Main execution
pdf_path = "C:\\Users\\Nikol\\Downloads\\lecture 7.pdf"
output_folder = "C:\\Users\\Nikol\\Downloads\\lecture7-filtered"

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
