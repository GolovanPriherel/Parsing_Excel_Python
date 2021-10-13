import re

import numpy as np
import urllib.request

# Считывание пдф файла
import fitz

# Регулярные выражения 1
Patt_Names = ('•\s(.+) [(][a-zA-Z,. ]{4,}[)][:]')
Patt_Names1 = ('•\s(Viagra) [(][a-zA-Z,. ]{4,}[)]')
Patt_Sells_US = ('U.S.\s[$]\s([0-9,—]+)\s[$]\s([0-9,—]+)\s[0-9()*—]+')
Patt_Sells_Int = ('International\s([0-9,—]+)\s([0-9,—]+)\s[0-9()*—]+\s[0-9()*—]+')
Patt_Sells_World = ('Worldwide revenues\s[$]\s([0-9,—]+)\s[$]\s([0-9,—]+)\s[0-9()*—]+')

pattall = [Patt_Names, Patt_Names1, Patt_Sells_US, Patt_Sells_Int, Patt_Sells_World]

def Find_Financial (PDF_File, AllPatts): # считывает постранично пдф и сразу же ищет вхождения регулярных выражений
    AllFinds = np.array([1])
    pdf_document = PDF_File
    doc = fitz.open(pdf_document)
    for pages in range(doc.pageCount):
        page = doc.loadPage(pages)
        page_text = page.getText("text")
        for patterns in AllPatts:
            result_sells = re.findall(patterns, page_text)
            if result_sells != []:
                print(pages, result_sells)

    return AllFinds

url = 'https://s21.q4cdn.com/317678438/files/doc_financials/2018/ar/Pfizer-2019-Financial-Report.pdf'
# url = 'https://s21.q4cdn.com/317678438/files/doc_financials/Annual/2018/2018-Financial-Report.pdf'

def Financial_Report (url): # Просто впиши ссылку на ПДФ и всё
    pdfname = 'INDFin.pdf'
    urllib.request.urlretrieve(url, '../Pdf_Storage/INDFin.pdf') # Скачиваем ПДФ
    Find_Financial('../Pdf_Storage/INDFin.pdf', pattall)

Financial_Report(url)