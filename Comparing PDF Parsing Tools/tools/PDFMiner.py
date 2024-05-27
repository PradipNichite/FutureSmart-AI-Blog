from pdfminer.high_level import extract_text

def pdfminer_extract(pdf_path):
  """Extracts text using pdfminer.six."""
  with open(pdf_path, 'rb') as pdf_file:
    text = extract_text(pdf_file)
    return text