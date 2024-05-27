import boto3
from dotenv import load_dotenv
import os
from PIL import Image
import fitz  # PyMuPDF

AWS_ACCESS_KEY_ID=  # Give the access key
AWS_SECRET_ACCESS_KEY= # Give Secret Access key

# Create a boto3 session with access keys
session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
textract_client = session.client('textract',region_name='us-east-1')


def textract_extract(pdf_path):
    """Extracts text using Amazon Textract with access keys."""
    import io

    pdf_document = fitz.open(pdf_path)
    pages = ""

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_data = page.get_pixmap().tobytes()

        with io.BytesIO(image_data) as img_buffer:
            response = textract_client.detect_document_text(Document={'Bytes': img_buffer.read()})

# We can take other data also but for simplicity I have took only word and line
# specifiy "pages" variable as output you wanted as i need only text so i took it
# as a sting if you want in json you can modify accordingly


        blocks = response['Blocks']
        text = ""

        for block in blocks:
            if block['BlockType'] in ['WORD']:
                text += block['Text'] + ' '
        pages+="/n"+text  # Add newline for readability

    return pages