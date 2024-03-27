import pytesseract
from PIL import Image

# Open the image file
image = Image.open("/Users/ayamaged/Self-Study/cs diploma/Gradution Project/tax-docs/commercial reg./العبور-1615488130-0.jpg")

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image, lang='ara')

# Print the extracted text
print(text)

