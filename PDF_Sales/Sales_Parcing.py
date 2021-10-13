import tabula
import fitz
import numpy as np
import Sales_Funcs as mf

def parse_pdf(file: str, start: str, end: str):
    """
    Находит страницы в пдф-файле, на которых есть таблицы между строками start и end
    :param file:
    :param start:
    :param end:
    :return:
    """
    with fitz.open(file) as doc:
        pages = []
        for i in range(len(doc)):  # номер страницы
            extract_dict = doc[i].get_textpage().extractDICT()
            # print(extract_dict)
            for block in extract_dict.get("blocks"):
                for span in block["lines"]:
                    # print(span["spans"][0]["text"])
                    if span["spans"][0]["text"] == start:
                        pages.append(i+1)
                    elif span["spans"][0]["text"] == end and len(pages) != 0:
                        pages.append(i+1)
                        return pages

# GSK = [Pharmaceutical turnover by therapeutic area, Pharmaceuticals]
# Pfizer = [Revenues—Selected Product Discussion, * Calculation is not meaningful or results are equal to or greater than 100%.]

def create_tables(path_to_pdf, start, stop):
    """
    Находит страницы с таблицами и возвращает таблицы в виде dataframe
    :param path_to_pdf:
    :return:
    """
    pages = parse_pdf(file=path_to_pdf, start=start, end=stop)

    # print(pages)

    if pages == None:
        return pages

    # tabula.convert_into(path_to_pdf, 'CVS_PDF.json', pages=pages, output_format='json', java_options=None)
    data_set = tabula.read_pdf(path_to_pdf, output_format='dataframe', pandas_options=({'header': None}),
                               pages=pages, stream=True, lattice=False)
    # for datas in data_set:
    #     for i in range(0, datas.shape[1]):
    #         print(datas[:,i])

    if data_set:
        return data_set

def prepering_data(data_set):
    """
    Получает таблицы dataframe и пересобирает строки в лист
    :param data_set:
    :return:
    """

    result_list = []
    for tables in data_set:
        sells_table = tables.fillna('')
        sells_table = np.array(sells_table)
        # print(sells_table)
        for i in range(sells_table.shape[0]):
            result = ''
            for j in range(sells_table.shape[1]):
                if sells_table[i][j] != '':
                    result += sells_table[i][j] + ' '
            result = result[0:-1]
            result_list.append(result + '\n')
    return result_list

def spacy_prepering_data(result_list, nlp):
    """
    Обработка пересобранного листа с помощью обученной в модуле Annual_Module_Training моделью spacy
    :param result_list:
    :param nlp:
    :return:
    """
    sells_list = []

    for lines in result_list:
        sells = mf.text_labels(lines, nlp)
        sells_list.append(sells)
        # print(sells)
    return sells_list

