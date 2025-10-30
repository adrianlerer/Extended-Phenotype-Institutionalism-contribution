#!/usr/bin/env python3
import PyPDF2
import sys

def extract_text_from_pdf(pdf_path, output_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = []
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text.append(f"\n{'='*80}\n")
            text.append(f"PAGE {page_num + 1}\n")
            text.append(f"{'='*80}\n")
            text.append(page.extract_text())
        
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(''.join(text))
        
        print(f"Extracted {len(pdf_reader.pages)} pages to {output_path}")

if __name__ == "__main__":
    extract_text_from_pdf("HETERONOMOUS_BAYESIAN_UPDATING_v2.pdf", "HETERONOMOUS_BAYESIAN_UPDATING_v2.txt")
