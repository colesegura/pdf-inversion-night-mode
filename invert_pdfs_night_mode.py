import fitz  # PyMuPDF library
import os
from PIL import Image, ImageOps

# Function to invert colors and adjust for night mode (reduce blue light)
def invert_pdf_colors(input_pdf, output_pdf):
    # Open the original PDF
    pdf_document = fitz.open(input_pdf)
    
    # Create a new PDF to hold the modified pages
    inverted_pdf = fitz.open()

    # Process each page in the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # Convert the pixmap to an image using Pillow
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Invert the colors
        img = ImageOps.invert(img)

        # Apply a filter to reduce blue light (make it warmer for night use)
        red, green, blue = img.split()

        # Reduce the blue channel intensity
        blue = blue.point(lambda b: b * 0.5)

        # Merge the channels back
        img = Image.merge("RGB", (red, green, blue))

        # Save the inverted and adjusted image as a temporary file
        temp_image_path = f"inverted_page_{page_num}.png"
        img.save(temp_image_path)

        # Insert the image back into the PDF
        img_pdf = fitz.open(temp_image_path)
        pdf_bytes = img_pdf.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdf_bytes)
        inverted_pdf.insert_pdf(img_pdf)

        # Remove the temporary image file
        os.remove(temp_image_path)

    # Save the inverted PDF
    inverted_pdf.save(output_pdf)
    inverted_pdf.close()

# Function to process multiple PDFs in a directory
def process_multiple_pdfs(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):  # Process only PDFs
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, f"inverted_{filename}")
            
            print(f"Inverting: {filename}")
            invert_pdf_colors(input_path, output_path)
            print(f"Saved inverted file as: {output_path}")

if __name__ == "__main__":
    # Change this to your PDF folder
    pdf_folder = ""
    
    # Process all PDFs in the specified folder
    process_multiple_pdfs(pdf_folder)