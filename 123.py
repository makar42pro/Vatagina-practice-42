# ==========================================
# Проверка ОДНОГО файла PDF/JPG/PNG
# Без сторонних библиотек
# ==========================================

import os
import subprocess

# Укажи путь к файлу
FILE = r"C:\Docs\document.pdf"

# Файл результата
OUTPUT = r"C:\Docs\result.txt"


def scan_pdf(file):
    try:
        with open(file, "rb") as f:
            data = f.read().decode(errors="ignore")
            return data[:10000]
    except:
        return "Ошибка чтения PDF"


def scan_image(file):
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
        return subprocess.check_output(
            ["powershell", "-Command", ps],
            text=True,
            encoding="utf-8"
        )
    except:
        return "Ошибка OCR"


# Определяем тип файла
ext = os.path.splitext(FILE)[1].lower()

if ext == ".pdf":
    result = scan_pdf(FILE)

elif ext in [".jpg", ".jpeg", ".png"]:
    result = scan_image(FILE)

else:
    result = "Неподдерживаемый формат"

# Сохраняем результат
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(result)

print("Готово.")
print("Результат:", OUTPUT)
