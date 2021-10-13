import re, fitz, pytesseract, urllib.request
#  ---- Работа с PDF
from PIL import Image

# Шаблоны поиска
patternsIND = [' IND ([0-9,]+)', ' IND Number.([0-9,]+)', ' IND No. ([0-9,]+)']
patternsINDDate = ['IND\D{4}(\d{1,2}.\d{1,2}.\d{1,4})', 'IND \d{5,6}..(\d{1,2}.\D+.\d{1,4})',
                   'IND\D{4}(\d{1,2}.\D+.\d{1,4})', 'IND \d{5,6}..(\d{1,2}.\d{1,2}.\d{1,4})',
                   'IND.[0-9,]+.Review #01 dated\s\s(\w+.\d+..\d+)', 'was originally submitted']

# Путь для подключения tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Открывает по страницам ПДФ (для текста)
def Extract_PDF_Text(pdf_file):
    pdf_document = pdf_file
    doc = fitz.open(pdf_document)
    for pages in range(doc.pageCount):
        page = doc.loadPage(pages)
        page_text = page.getText("text")
        yield page_text
        # print(page_text)

# Находит в тексте из ПДФ-а номер и дату
def extract_text(pdf_file, pattern1, pattern2):
    Date, IND = [], []
    for page in Extract_PDF_Text(pdf_file):
        for patt in pattern1:
            result_IND = re.findall(patt, page)
            for sub in range(len(result_IND)):
                IND.append(result_IND[sub].replace('\n', ''))
        for patt in pattern2:
            result_IND_Date = re.findall(patt, page)
            for sub in range(len(result_IND_Date)):
                Date.append(result_IND_Date[sub].replace('\n', ''))
    if IND:
        IND = (max(set(IND), key=IND.count))
    if Date:
        Date = (max(set(Date), key=Date.count))
    elif IND and Date:
        IND = (max(set(IND), key=IND.count))
        Date = (max(set(Date), key=Date.count))

    # print('Текст победил')
    return IND, Date

# Получает картинки из ПДФ-а
def extract_png(PDF):
    ind_num, ind_date = '',''
    doc = fitz.open(PDF)
    for i in range(0, len(doc)):
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
            if IND_Num and IND_Date:
                return IND_Num, IND_Date
            elif IND_Num:
                ind_num = IND_Num
            elif IND_Date:
                ind_date = IND_Date

    return ind_num, ind_date

# Распознавание текста в картинках
def Find_IND_Date_Tess(picture):
    img = Image.open(f'{picture}')
    file_name = img.filename
    file_name = file_name.split(".")[0]
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

# Находит из картинок номер и дату
def extract_text_png(text, pattern1, pattern2):
    IND, Date = [], []
    for patt in pattern1:
        result_IND = re.findall(patt, text)
        for sub in range(len(result_IND)):
            IND.append(result_IND[sub].replace('\n', ''))
    for patt in pattern2:
        result_IND_Date = re.findall(patt, text)
        for sub in range(len(result_IND_Date)):
            Date.append(result_IND_Date[sub].replace('\n', ''))

    if IND:
        IND = (max(set(IND), key=IND.count))
    elif Date:
        Date = (max(set(Date), key=Date.count))
    elif IND and Date:
        IND = (max(set(IND), key=IND.count))
        Date = (max(set(Date), key=Date.count))

    # print('Изображения победили')
    return IND, Date

# Вызов всех ф-ий для парсера
def Find_IND_Date (url): # Просто впиши ссылку на ПДФ и всё
    urllib.request.urlretrieve(url, "../IND1.pdf")     # Скачиваем ПДФ
    IND_Num, IND_Date = extract_text("../IND1.pdf", patternsIND, patternsINDDate)  # Зырим текст
    TrueNum, TrueDate = None, None

    if IND_Num and IND_Date:    # Проверям хватит ли только текста для проверки
        return IND_Num, IND_Date
    elif IND_Num:
        TrueNum = IND_Num
    elif IND_Date:
        TrueDate = IND_Date

    else:
        IND_Num1, IND_Date1 = extract_png("IND1.pdf") # Проверка с помощью распознавания

        if IND_Num1:
            TrueNum = IND_Num1
        elif IND_Date1:
            TrueDate = IND_Date1
    # Доделать распознавание приколсов

    return TrueNum, TrueDate

# Проверенные ссылки на пдф
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2013/202971Orig1s000PharmR.pdf'                 # с инд (5 цифр) и датой (через пробел)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/212887Orig1s000,212888Orig1s000Approv.pdf' # с инд (6)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2012/202428Orig1s000PharmR.pdf'                 # с инд (6)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2002/21-456_Aciphex_Medr_P1.pdf'                # Картинка с датой IND, но без номера
url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2010/022518Orig1s000PharmR.pdf'                   # Куча разных номеров инд с датой

IND_Num, IND_Date = Find_IND_Date(url)
print(IND_Num, '|', IND_Date)