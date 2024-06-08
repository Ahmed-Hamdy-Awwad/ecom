import pytesseract
from PIL import Image
import os
from django.conf import settings
import easyocr
import re
import cv2

from math import ceil


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

    ######### Tesseract ################
    image = Image.open(temp_path)
    text = pytesseract.image_to_string(image, lang="ara")

    count = 1
    for line in text.splitlines():
        if line:
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

    ######## EasyOCR ############
    full_results, tax_number_results, industry_results = process_eacyosr(temp_path)
    if industry_results:
        data["industry"] = industry_results[0]
        last_industry_word = data.get("industry").split(" ")[-1]

    count = 1
    industry_line_no = None
    for line in full_results:
        line = line[1]
        if line:
            if last_industry_word in line:
                industry_line_no = count
            if industry_line_no and count == (industry_line_no + 1):
                data["tax_number"] = line
                break

        count += 1

    if not data.get("tax_number") or (
        data.get("tax_number")
        and tax_number_results
        and (
            len(data.get("tax_number").replace(" ", ""))
            < len(tax_number_results[0].replace(" ", ""))
        )
    ):
        data["tax_number"] = clearNumbers(tax_number_results[0])

    if os.path.exists(temp_path):
        os.remove(temp_path)
    return data


def process_eacyosr(temp_path):
    image = cv2.imread(temp_path)
    tax_number_section = get_crop_section("tax_number", image)
    industry_section = get_crop_section("industry", image)
    reader = easyocr.Reader(
        ["ar"],
        gpu=True,
    )
    full_results = reader.readtext(image)
    tax_number_results = reader.readtext(tax_number_section, paragraph=True, detail=0)
    industry_results = reader.readtext(industry_section, paragraph=True, detail=0)
    return full_results, tax_number_results, industry_results


CROP_DIMENSIONS = {
    "industry": {
        "x1": 490,
        "y1": 350,
        "x2": 878,
        "y2": 400,
    },
    "tax_number": {
        "x1": 0,
        "y1": 400,
        "x2": 900,
        "y2": 450,
    },
}


def get_crop_section(type, image):
    """Return cropped section"""
    crop_dimensions = CROP_DIMENSIONS.get(type)

    if crop_dimensions:
        scale = image.shape[1] / 878

        x1, y1, x2, y2 = crop_dimensions.values()

        x1 = ceil(scale * x1)
        y1 = ceil(scale * y1)
        x2 = ceil(scale * x2)
        y2 = ceil(scale * y2)

        return image[y1:y2, x1:x2]

    return None
