import pytesseract
from PIL import Image
import os
from django.conf import settings
import easyocr
import re


def clearLetters(line):
    clean_line = line
    for c in line:
        if not re.match(r"^[ء-ي]+$", c):
            clean_line = clean_line.replace(c, " ")
    clean_line = clean_line.replace("  ", " ").strip()
    return clean_line


def clearLettersNumbers(line):
    clean_line = line
    for c in line:
        if not re.match(r"^([ء-ي]|[٠-٩])+$", c):
            clean_line = clean_line.replace(c, " ")
    clean_line = clean_line.replace("  ", " ").strip()
    return clean_line


def clearNumbers(line):
    clean_line = line
    for c in line:
        if not (c in "٠١٢٣٤٥٦٧٨٩ -"):
            clean_line = clean_line.replace(c, " ")
    clean_line = clean_line.replace("  ", " ")
    return clean_line


def process(file):
    data = {
        "name": "",
        "owner": "",
        "address": "",
        "tax_number": "",
        "industry": "",
    }
    temp_path = os.path.join(settings.BASE_DIR, file.name)
    with open(temp_path, "wb") as binary_file:
        # Write bytes to file
        binary_file.write(file.file.getvalue())

    image = Image.open(temp_path)
    text = pytesseract.image_to_string(image, lang="ara")

    count = 1
    for line in text.splitlines():
        if line:
            print(count, line)
            match (count):
                case 4:
                    data["name"] = clearLetters(line)
                case 5:
                    data["owner"] = clearLetters(line)
                case 6:
                    data["address"] = clearLettersNumbers(line)
                case 8:
                    data["industry"] = clearLetters(line)
            count += 1

    reader = easyocr.Reader(
        ["ar"]
    )  # this needs to run only once to load the model into memory
    result = reader.readtext(
        image,
    )  # best -0,1, -0.2
    # result = reader.readtext(image, detail=0, y_ths=-0.2)

    count = 1
    max_seq_numbers = None
    for line in result:
        line = line[1]
        if line:
            if not max_seq_numbers:
                max_seq_numbers = clearNumbers(line) or None
                continue
            if len(max_seq_numbers) < len(clearNumbers(line)):
                max_seq_numbers = clearNumbers(line)
    if max_seq_numbers and len(max_seq_numbers.strip()) <= 21:
        data["tax_number"] = max_seq_numbers

    if os.path.exists(temp_path):
        os.remove(temp_path)
    return data
