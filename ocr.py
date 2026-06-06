import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_and_dob(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    dob_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
    dob = dob_match.group(0) if dob_match else None
    return text, dob

