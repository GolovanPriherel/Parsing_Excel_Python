import re, fitz, pytesseract, urllib.request
#  ---- Работа с PDF
from PIL import Image

# Шаблоны поиска
patterns_indication = ['Indication[(s)]+?.?\s(.+)\s?', 'Indication[(s)/Population]+?.?\s(.+\s?.{0,})']

# Applicant Proposed
# Indication(s)/Population(s)
# Treatment of adult patients with acute bacterial skin and skin structure
# infections (ABSSSI)

# Путь для подключения tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Открывает по страницам ПДФ (для текста)
def extract_PDF_Text(pdf_file):
    pdf_document = pdf_file
    doc = fitz.open(pdf_document)
    for pages in range(doc.pageCount):
        page = doc.loadPage(pages)
        page_text = page.getText("text")
        yield page_text
        # print(page_text)

# Находит в тексте из ПДФ-а номер и дату
def extract_text(pdf_file, pattern1):
    IND = []
    for page in extract_PDF_Text(pdf_file):
        for patt in pattern1:
            result_IND = re.findall(patt, page)
            for sub in range(len(result_IND)):
                IND.append(result_IND[sub].replace('\n', ''))

    if IND:
        IND = (max(set(IND), key=IND.count))
    # print('Текст победил')
    return IND

# Получает картинки из ПДФ-а
def extract_png(PDF):
    IND_Num = []
    doc = fitz.open(PDF)
    for i in range(0, 6):
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
            IND_Num = extract_text_png(text, patterns_indication)

    return IND_Num

# Распознавание текста в картинках
def Find_IND_Date_Tess(picture):
    img = Image.open(f'{picture}')
    file_name = img.filename
    file_name = file_name.split(".")[0]
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

# Находит из картинок номер и дату
def extract_text_png(text, pattern1):
    IND = []
    for patt in pattern1:
        result_IND = re.findall(patt, text)
        for sub in range(len(result_IND)):
            IND.append(result_IND[sub].replace('\n', ''))

    if IND:
        IND = (max(set(IND), key=IND.count))
    # print('Изображения победили')
    return IND

# Вызов всех ф-ий для парсера
def Find_IND_Date (url): # Просто впиши ссылку на ПДФ и всё
    urllib.request.urlretrieve(url, "../Pdf_Storage/INDIndic.pdf")     # Скачиваем ПДФ
    IND_Num = extract_text("../Pdf_Storage/INDIndic.pdf", patterns_indication)  # Зырим текст
    TrueNum = None

    if IND_Num:    # Проверям хватит ли только текста для проверки
        return IND_Num

    else:
        IND_Num1 = extract_png("INDIndic.pdf") # Проверка с помощью распознавания

        if IND_Num1:
            TrueNum = IND_Num1

    return TrueNum

# Проверенные ссылки на пдф
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2013/202971Orig1s000PharmR.pdf'                 # с инд (5 цифр) и датой (через пробел)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/212887Orig1s000,212888Orig1s000Approv.pdf' # с инд (6)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2012/202428Orig1s000PharmR.pdf'                 # с инд (6)
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2002/21-456_Aciphex_Medr_P1.pdf'                # Картинка с датой IND, но без номера
# url = 'https://www.accessdata.fda.gov/drugsatfda_docs/nda/2010/022518Orig1s000PharmR.pdf'                 # Куча разных номеров инд с датой
url = "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2017/208610Orig1s000,208611Orig1s000MedR.pdf"     # Индикация

IND_Num = Find_IND_Date(url)
print(IND_Num)