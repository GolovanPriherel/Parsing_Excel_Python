import re, fitz, pytesseract
from PIL import Image
from dateutil.parser import parse
import datetime

pattern_ind = ['\sIND\s{1,}([0-9,-]+)', '\sIND\sNumber.?\s?([0-9,-]+)', '\sIND No\s?([0-9,-]+)']
pattern_date = ['IND\s{1,}[0-9,-—]+\s{1,}Review\s{1,}#01\s{1,}dated\s{1,}([0-9a-zA-Z.]+.[0-9a-zA-Z]+.\s?\d+)',
                'IND\s{1,}[0-9,-—]+\s{1,}on\s{1,}(\d+.[0-9a-zA-Z]+.\d+)', 'IND\s{1,}[0-9,-—]+\s{1,}.(\d+\s{1,}[0-9a-zA-Z]+\s{1,}\d+)']
                # 'was\s*[Ooriginaly]*\s*submitted\s*[oni]*\s*(\d+[/\-.]\d+[/\-.]\d+)']
pattern_indic = ['Indication:\s{1,}([a-zA-Z ]+)']

# pattern_date = ['IND\D{4}(\d{1,2}.\d{1,2}.\d{1,4})', 'IND \d{5,6}..(\d{1,2}.\D+.\d{1,4})',
#                    'IND\D{4}(\d{1,2}.\D+.\d{1,4})', 'IND \d{5,6}..(\d{1,2}.\d{1,2}.\d{1,4})',
#                    'IND.[0-9,]+.Review #01 dated\s\s(\w+.\d+..\d+)']
# , '[Ii]ndication[(s)/Population]+?.?\s(.+\s?.{0,})'

all_patterns = [pattern_ind, pattern_date, pattern_indic]

# Путь для подключения tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Открывает по страницам ПДФ (для текста)
def extract_pdf_text(pdf_file):
    pdf_document = pdf_file
    doc = fitz.open(pdf_document)
    for pages in range(doc.pageCount):
        page = doc.loadPage(pages)
        page_text = page.getText("text")
        yield page_text

def Find_IND_Date_Tess(picture):
    img = Image.open(f'{picture}')
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

def find_regular(text, allpats, all_vall):
    col = 0
    for patt in allpats:
        for elem in patt:
            result_ind = re.findall(elem, text)
            if result_ind:
                for finds in result_ind:
                    finds = str(finds).replace('\n', '')
                    all_vall[col] += finds + '---'
        col += 1
    return all_vall

# Находит в тексте из ПДФ-а номер и дату
def extract_text(pdf_file, all_pats, all_vall):

    for page in extract_pdf_text(pdf_file):     # Этап поиска текста
        all_vall = find_regular(page, all_pats, all_vall)

    for i in range(len(all_vall)):
        all_vall[i] = all_vall[i][0:-3]

    print(all_vall)

    t, ch = 0, 0
    for vall in all_vall:
        all_vall = sort_max(all_vall)
        t += 1
        if vall:
            ch += 1
        if t == len(all_pats):
            return all_vall

    doc = fitz.open(pdf_file)
    for i in range(0, len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:  # this is GRAY or RGB
                pix.writePNG("Text1.png")
            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("Text1.png")
            text = Find_IND_Date_Tess("Text1.png")
            all_vall = find_regular(text, all_pats, all_vall)

    for vall in all_vall:
        if vall:
            sort_max(all_vall)

    return all_vall

def sort_max(all_vall):
    iter = 0
    for lists in all_vall:
        find_max = re.split('---', lists)
        all_vall[iter] = (max(set(find_max), key=find_max.count))
        iter += 1
    return all_vall

def correct_time(all_vall):
    date_list = all_vall[1]
    date = date_list
    if date:
        date_def = parse(date)
    else:
        return all_vall
    date = str(date_def.date()).split('-')
    date_obj = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    final_date = date_obj.strftime('%m.%d.%Y').replace('/', '.')
    all_vall[1] = final_date
    return all_vall