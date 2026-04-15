# ==========================================
# Python скрипт для сканирования PDF и JPG
# Извлекает текст из PDF + OCR из JPG/JPEG
# Требуется:
# pip install pytesseract pdfplumber pillow
# Также установлен Tesseract OCR
# ==========================================

import os
import pdfplumber
import pytesseract
from PIL import Image

# Папка с файлами
FOLDER = r"C:\Docs"

# Путь к tesseract.exe (если нужно)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Файл результата
OUTPUT_FILE = r"C:\Docs\scan_result.txt"


def scan_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = f"Ошибка PDF: {e}"
    return text


def scan_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang="rus+eng")
        return text
    except Exception as e:
        return f"Ошибка JPG: {e}"


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        for root, dirs, files in os.walk(FOLDER):
            for file in files:

                path = os.path.join(root, file)
                ext = file.lower().split(".")[-1]

                out.write("\n=============================\n")
                out.write(f"Файл: {path}\n")
                out.write("=============================\n")

                if ext == "pdf":
                    text = scan_pdf(path)

                elif ext in ["jpg", "jpeg", "png"]:
                    text = scan_image(path)

                else:
                    continue

                out.write(text + "\n")

    print("Сканирование завершено.")
    print("Результат:", OUTPUT_FILE)


if name == "main":
    main()
