import pdfplumber

def pdfplumber_extract(pdf_path):
  """Extracts text using pdfplumber."""
  with pdfplumber.open(pdf_path) as pdf:
    text = ''
    for page in pdf.pages:
      text += page.extract_text()
    return text