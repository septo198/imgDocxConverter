from PIL import Image
import pytesseract
from docx import Document
from fpdf import FPDF
import os

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    return text

def save_text_to_docx(text, output_path):
    # Create a Word Document
    doc = Document()
    # Split the text into lines
    lines = text.split('\n')
    # Iterate over lines to respect indentation and paragraphs
    for line in lines:
        if line.strip():  # If the line is not empty
            doc.add_paragraph(line)
        else:
            doc.add_paragraph('')  # Add an empty paragraph for double newlines
    # Save the document
    doc.save(output_path)

def save_text_to_pdf(text, output_path):
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Split the text into lines
    lines = text.split('\n')
    # Iterate over lines to respect indentation and paragraphs
    for line in lines:
        pdf.multi_cell(0, 10, line)
    # Save the PDF
    pdf.output(output_path)

def convert_image_to_text_doc(image_path, output_format='docx', generate_pdf=False):
    # Extract text from image
    text = extract_text_from_image(image_path)
    
    # Determine output file paths
    base_filename = os.path.splitext(image_path)[0]
    docx_path = base_filename + '.docx'
    pdf_path = base_filename + '.pdf'
    
    # Save the extracted text to the chosen document format
    if output_format == 'docx':
        save_text_to_docx(text, docx_path)
    elif output_format == 'odt':
        # Placeholder: implement ODT saving if needed, currently we are using docx
        save_text_to_docx(text, docx_path)
    else:
        raise ValueError("Unsupported output format. Use 'docx' or 'odt'.")
    
    # Optionally, generate a PDF copy
    if generate_pdf:
        save_text_to_pdf(text, pdf_path)

    # Return the paths of generated files
    if generate_pdf:
        return docx_path, pdf_path
    else:
        return docx_path

# Example usage
image_path = '/home/matteo/Downloads/screenshot.jpeg'  # Replace with your screenshot image path
output_format = 'docx'  # Choose 'docx' or 'odt'
generate_pdf = True  # Set to True to generate both docx/odt and pdf, False otherwise

# Convert the image and get output file paths
output_files = convert_image_to_text_doc(image_path, output_format, generate_pdf)
print("Generated files:", output_files)
