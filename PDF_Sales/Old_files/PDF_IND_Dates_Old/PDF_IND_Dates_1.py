import io
import re

#  ---- Работа с PDF
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import fitz

from PIL import Image
import pytesseract

patternsIND = [' IND (\d{5,6})', ' IND Number.{6,7}']
patternsINDDate = ['IND\D{4}(\d{1,2}.\d{1,2}.\d{1,4})', 'IND \d{5,6}..(\d{1,2}.\D+.\d{1,4})',
                   'IND\D{4}(\d{1,2}.\D+.\d{1,4})', 'IND \d{5,6}..(\d{1,2}.\d{1,2}.\d{1,4})']

# Путь для подключения tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def Find_IND_Date_Tess(picture):
	img = Image.open(f'{picture}')
	file_name = img.filename
	file_name = file_name.split(".")[0]
	custom_config = r'--oem 3 --psm 6'
	text = pytesseract.image_to_string(img, config=custom_config)
	return text

def extract_png(PDF):
    list1, list2 = [], []
    doc = fitz.open(PDF)
    for i in range(10, len(doc)-40):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("Text1.png")
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("Text1.png")
                pix1 = None
            pix = None
            text = Find_IND_Date_Tess("Text1.png")
            IND_Num, IND_Date = extract_text_png(text, patternsIND, patternsINDDate)
            # print('---', i)
            if (IND_Num != None):
                list1.append(IND_Num)
            if (IND_Date != None):
                list1.append(IND_Date)

    return list1, list2

# Считывание пдф файла
def extract_text_by_page(pdf_file):
    with open(pdf_file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

# Ф-ия считывания
def extract_text(pdf_file, pattern1, pattern2):
    IND, Date = None, None
    for page in extract_text_by_page(pdf_file):
        for patt in pattern1:
            result_IND = re.search(patt, page, re.M | re.I)
            if (result_IND != None):
                IND = result_IND.group(0)
        for patt in pattern2:
            result_IND_Date = re.search(patt, page, re.M | re.I)
            if (result_IND_Date != None):
                Date = result_IND_Date.group(1)

    return IND, Date

def extract_text_png(text, pattern1, pattern2):
    IND, Date = None, None
    for patt in pattern1:
        result_IND = re.search(patt, text, re.M | re.I)
        if (result_IND != None):
            IND = result_IND.group(0)
    for patt in pattern2:
        result_IND_Date = re.search(patt, text, re.M | re.I)
        if (result_IND_Date != None):
            Date = result_IND_Date.group(1)

    return IND, Date


import urllib.request

# Ссылка на пдф
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2013/202971Orig1s000PharmR.pdf'                 # с инд (5 цифр) и датой (через пробел)
url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/212887Orig1s000,212888Orig1s000Approv.pdf' # с инд (6)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2012/202428Orig1s000PharmR.pdf'                 # с инд (6)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2002/21-456_Aciphex_Medr_P1.pdf'                  # Картинка с датой IND, но без номера

# Нипасредстна вызов функции

def Find_IND_Date (url): # Просто впиши ссылку на ПДФ и всё
    urllib.request.urlretrieve(url, "../IND1.pdf") # Скачиваем ПДФ
    IND_Num, IND_Date = extract_text("../IND1.pdf", patternsIND, patternsINDDate) # Зырим текст
    if (IND_Num != None) and (IND_Date != None): # Проверям хватит ли только текста для проверки
        return IND_Num, IND_Date
    IND_Num1, IND_Date1 = extract_png("IND1.pdf") # Проверка с помощью распознавания
    return IND_Num1, IND_Date1

IND_Num, IND_Date = Find_IND_Date(url)
print(IND_Num, IND_Date)
