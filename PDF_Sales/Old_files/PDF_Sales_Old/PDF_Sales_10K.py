import re
import urllib.request

# Считывание пдф файла
import fitz

# Границы таблиц
# Patt_Table = ('U.S.\s{0,}[$]?\s{0,}([0-9,—]+)\s{0,}[$]?\s{0,}([0-9,—]+)\s{0,}[$]?\s{0,}([0-9,—]+)')

Patt_Hat = ('U.S.(?:\s*([0-9,—N/A*—]+)+)*')

# Patt_Table = ('([a-zA-Z()/ ]+)\s{0,}[$]?\s{0,}([0-9,—]+)\s{0,}[$]?\s{0,}([0-9,—]+)\s{0,}[$]?\s{0,}([0-9,—]+)?\s{0,}[()0-9%N/A*— ]+\s{0,}'
#               'U.S.\s{0,}([0-9,—]+)\s{0,}([0-9,—]+)\s{0,}([0-9,—]+)?\s{0,}[0-9()N/A*— ]+\s{0,}[%]?\s{0,}'
#               'Non-U.S.\s{0,}([0-9,—]+)\s{0,}([0-9,—]+)\s{0,}([0-9,—]+)?\s{0,}[()0-9N/A*— ]+\s{0,}[%]?\s{0,}')

# p1 = '/([0-9%()*—]+\s*[%])'

# Opdivo $ 6,735 $ 4,948 $ 3,774 36 % 31 %
# U.S. 4,239 3,102 2,664 37 % 16 %
# Non-U.S. 2,496 1,846 1,110 35 % 66 %

# Регулярные выражения 1
# Patt_Names = ('\s([A-Za-z]+\s?\d{0,2})\s[$][0-9,]{3,}\s[UpDown0-9%*]+\s')
# Patt_Sells_US = ('U.S.\s[$]\s{2}([0-9,—]+)\s{2}[$]\s{2}([0-9,—]+)\s{1,3}[0-9,—*()]')
# Patt_Sells_Int = ('Int’l.\s{1,3}([0-9,—]+)\s{1,4}([0-9,—]+)')
# Patt_Sells_World = ('Worldwide\s[$]\s{2}([0-9,—]+)\s{2}[$]\s{2}([0-9,—]+)\s{1,3}[0-9,—*()]')

# Регулярные выражения 2
# Patt2_All = ('\s([a-zA-Z/]+)\s[$]?\s?[0-9,—]+\s[$]?\s?[0-9,—]+\s{1,3}[(1-9)N/A*]+[%]?\s')
# Patt2_US = ('U.S.\s([0-9,—]+)\s\s([0-9,—]+)\s{1,3}[()0-9*N/A]+[%]?\s')
# Patt2_NonUS = ('Non-U.S.\s([0-9,—]+)\s\s([0-9,—]+)\s{1,3}[()0-9*N/A]+[%]?\s')

# Patt22_Names = ('\s([a-zA-Z/]+)\s[$]?\s?[0-9,—]+\s[$]?\s?[0-9,—]+\s{1,3}[(1-9)N/A*]+[%]?\s')
# Patt2_All2 = ('([a-zA-Z/]+)\s[$]?\s?[0-9,—]+\s[$]?\s?[0-9,—]+')
# Patt2_US2 = ('U.S.\s([0-9,—]+)\s([0-9,—]+)\s[0-9*N/A]+')
# Patt2_NonUS2 = ('Non-U.S.\s([0-9,—]+)\s([0-9,—]+)\s[0-9*N/A]+')

# pattall1 = [Patt_Names, Patt_Sells_US, Patt_Sells_Int, Patt_Sells_World]
pattall = [Patt_Hat]

# pattall = [Patt_Names, Patt_Sells_US, Patt_Sells_Int, Patt_Sells_World, Patt2_All, Patt2_US, Patt2_NonUS]

def Find_Annual (PDF_File, AllPatts2): # считывает постранично пдф и сразу же ищет вхождения регулярных выражений
    res_tab = []
    pdf_document = PDF_File
    doc = fitz.open(pdf_document)
    for pages in range(doc.pageCount):
        page = doc.loadPage(pages)
        page_text = page.getText("text")

        for patterns in AllPatts2:
            result_sells = re.findall('([a-zA-Z]+)(?:\s*\s*([0-9,—% ]+))+', page_text)
            if result_sells:
                print(result_sells)

    return res_tab

# Pzifer
# url = 'https://s21.q4cdn.com/317678438/files/doc_financials/2020/ar/PFE-2020-Form-10K-FINAL.pdf'

# Bristol
url = 'https://s21.q4cdn.com/104148044/files/doc_financials/annual_reports/2019/2019-10-K.pdf'
# url = 'https://s21.q4cdn.com/104148044/files/doc_financials/annual_reports/2020/BMS_10k_new.pdf'
# url = "https://s21.q4cdn.com/104148044/files/doc_financials/annual_reports/2018/2018-10-K.pdf"

def Annual_Report (url): # Просто впиши ссылку на ПДФ и всё
    urllib.request.urlretrieve(url, '../INDAnn.pdf') # Скачиваем ПДФ
    res_tab = Find_Annual('../INDAnn.pdf', pattall)
    return res_tab

res_tab = Annual_Report(url)
# for i in res_tab:
#     for y in i:
#         print(y)