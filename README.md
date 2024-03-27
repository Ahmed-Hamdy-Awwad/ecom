# ecom

Graduation project

Make sure to have your DB configuration in a dict with name "db_settings" in a file with name "db_conf.py" and place it in the ecom directory, the directory of settings.py

## FOR OCR

### Tesseract Engine

for more information https://tesseract-ocr.github.io/

#### MacOS:

    Step 1. Install Tesseract on your machine
        brew install tesseract [OCR Engine]
    Step 2. Install Language data
        brew install tesseract-lang [Other languages data including arabic]
    Step 3.
        pip install -r requirements.txt

#### Windows:

    Step 1. Install Tesseract on your machine
        Visit https://github.com/UB-Mannheim/tesseract/wiki and download Tesseract installer for Windows.
    Step 2. Install Language data
        Open https://github.com/tesseract-ocr/tessdata and download Arabic language.  ara.traineddata.
        Copy the downloaded file to the tessreact_ocr installation location, some location like: C:\Program Files\Tesseract-OCR\tessdata
