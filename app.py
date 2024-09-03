import argparse
from PIL import Image
import pytesseract
from docx import Document
from fpdf import FPDF
import os

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    lines = text.split('\n')
    processed_text = ""
    for line in lines:
        if line.strip():  
            processed_text += line.strip() + " "
        else:  
            processed_text = processed_text.strip() + "\n"
    return processed_text.strip()

def save_text_to_docx(text, output_path):
    doc = Document()
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            doc.add_paragraph(line)
        else:
            doc.add_paragraph('')
    doc.save(output_path)

def save_text_to_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Cambria", size=12)
    lines = text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path)

def convert_image_to_text_doc(image_path, generate_pdf=False):
    text = extract_text_from_image(image_path)
    
    base_filename = os.path.splitext(image_path)[0]
    docx_path = f"{base_filename}.docx"
    pdf_path = f"{base_filename}.pdf"

    save_text_to_docx(text, docx_path)
    
    if generate_pdf:
        save_text_to_pdf(text, pdf_path)

    if generate_pdf:
        return docx_path, pdf_path
    else:
        return docx_path

def main():
    parser = argparse.ArgumentParser(description="Convert image text to docx and optionally a PDF.")
    parser.add_argument("image_path", help="Path to the screenshot image containing text.")
    parser.add_argument("--generate_pdf", action="store_true", help="Generate a PDF copy of the text document.")
    
    args = parser.parse_args()
    
    output_files = convert_image_to_text_doc(args.image_path, args.generate_pdf)
    print("Generated files:", output_files)

if __name__ == "__main__":
    main()
