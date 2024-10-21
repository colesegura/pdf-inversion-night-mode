import fitz  # PyMuPDF library
import os
from PIL import Image, ImageOps, ImageEnhance

# Function to invert colors and adjust for visibility under red filter
def adjust_pdf_for_red_filter(input_pdf, output_pdf):
    # Open the original PDF
    pdf_document = fitz.open(input_pdf)
    
    # Create a new PDF to hold the modified pages
    adjusted_pdf = fitz.open()

    # Process each page in the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # Convert the pixmap to an image using Pillow
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Invert the colors (dark mode)
        img = ImageOps.invert(img)

        # Convert image to grayscale to ensure all text is visible
        img = ImageOps.grayscale(img)

        # Increase the contrast to make text stand out more
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)  # Adjust contrast (2.0 is a good starting point)

        # Save the adjusted image as a temporary file
        temp_image_path = f"adjusted_page_{page_num}.png"
        img.save(temp_image_path)

        # Insert the image back into the PDF
        img_pdf = fitz.open(temp_image_path)
        pdf_bytes = img_pdf.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdf_bytes)
        adjusted_pdf.insert_pdf(img_pdf)

        # Remove the temporary image file
        os.remove(temp_image_path)

    # Save the adjusted PDF
    adjusted_pdf.save(output_pdf)
    adjusted_pdf.close()

# Function to process multiple PDFs in a directory
def process_multiple_pdfs(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):  # Process only PDFs
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, f"red_filter_adjusted_{filename}")
            
            print(f"Adjusting colors for: {filename}")
            adjust_pdf_for_red_filter(input_path, output_path)
            print(f"Saved adjusted file as: {output_path}")

if __name__ == "__main__":
    # Change this to your PDF folder
    pdf_folder = "/Users/colesegura/Library/CloudStorage/Box-Box/ECE 383"
    
    # Process all PDFs in the specified folder
    process_multiple_pdfs(pdf_folder)