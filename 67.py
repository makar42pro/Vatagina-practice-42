# ==========================================
# Python скрипт БЕЗ сторонних библиотек
# Работает только со стандартным Python
# PDF и JPG через встроенный OCR Windows
# ==========================================

import os
import subprocess

# Папка для проверки
FOLDER = r"C:\Docs"

# Файл результата
OUTPUT = r"C:\Docs\scan_result.txt"


def scan_pdf(file):
    # Пытаемся открыть PDF как текст
    try:
        with open(file, "rb") as f:
            data = f.read().decode(errors="ignore")
            return data[:5000]   # первые символы
    except:
        return "Не удалось прочитать PDF"


def scan_image(file):
    # OCR через PowerShell + Windows OCR
    ps = f'''
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$img = [Windows.Storage.StorageFile]::GetFileFromPathAsync("{file}").GetAwaiter().GetResult()
$stream = $img.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult()
$decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bitmap = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
$ocr = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$res = $ocr.RecognizeAsync($bitmap).GetAwaiter().GetResult()
$res.Text
'''
    try:
        result = subprocess.check_output(
            ["powershell", "-Command", ps],
            text=True,
            encoding="utf-8"
        )
        return result
    except:
        return "OCR ошибка"


with open(OUTPUT, "w", encoding="utf-8") as out:

    for root, dirs, files in os.walk(FOLDER):
        for file in files:

            path = os.path.join(root, file)
            ext = file.lower().split(".")[-1]

            out.write("\n=====================\n")
            out.write(path + "\n")
            out.write("=====================\n")

            if ext == "pdf":
                text = scan_pdf(path)

            elif ext in ["jpg", "jpeg", "png"]:
                text = scan_image(path)

            else:
                continue

            out.write(text + "\n")

print("Готово:", OUTPUT)
