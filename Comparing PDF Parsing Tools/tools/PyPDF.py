import pypdf

def pypdf_extract(pdf_path):
  """Extracts text using pypdf"""
  with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = pypdf.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[page_num]
      text +="\n"+ page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
    return text