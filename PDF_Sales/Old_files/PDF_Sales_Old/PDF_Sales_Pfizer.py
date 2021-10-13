import fitz
import itertools
from collections import Counter


def parse_pdf(file: str):
    result: list[list[str]] = []
    with fitz.open(file) as doc:
        for i in range(len(doc)):  # номер страницы
            extract_dict = doc[i].get_textpage().extractDICT()
            # print(extract_dict)
            for block in extract_dict.get("blocks"):
                temp_list = []
                for span in block["lines"]:
                    temp_list.append(span["spans"][0]["text"])
                result.append(temp_list)
    return result


def remove_elem(source: list[str], deletes: list[str]):
    for delete in deletes:
        while source.count(delete) != 0:
            source.remove(delete)
    return source


def remove_spaces(res: list[str]) -> list:
    return [i.replace(" ", "") for i in res]


def unique_elem(o: list[str]) -> bool:
    """
    ['', '', '', 'Hello!'] -> Counter(''=3, 'Hello!'=1) -> 4 == 2 -> False
    ['A1', 'S2', 'R4', 'Hello!'] -> Counter('A1'=1, 'S2'=1, 'R4'=1, 'Hello!'=1) -> 4 == 4 -> True
    :param o:
    :return:
    """
    return True if len(Counter(remove_spaces(o))) == len(o) else False


def get_table(_result, start: list, end: list) -> list:
    products: list[list[str]] = []
    for _elem in _result:
        if _elem[0] in start:
            products.append(_elem)
        elif _elem[0] in end and len(products) != 0:
            return products
        elif len(products) != 0:
            products.append(_elem)

def columns_to_delete(products):
    t, cols_num = 0, []
    for cols in products[2]:
        if 'vs' in cols:
            t -= 1
            cols_num.append(t)
    cols_num.reverse()
    return cols_num

def max_length(products):
    max_len = len(products[5])
    return max_len


def prepare_table(_table, _len: int, skip_elems: list, remove_elems: list):
    """
    Before:
        ['Name', 'Price2018', 'Price2019']
        ['US', 'Price2018', 'Price2019']
        ['Non-US', 'Price2018', 'Price2019']
    After:
        ['Name', 'Name', 'Price2018', 'Price2019']
        ['US', 'Price2018', 'Price2019']
        ['Non-US', 'Price2018', 'Price2019']
    :param _table:
    :param skip_elems:
    :param remove_elems:
    :return:
    """
    final: list = []
    for elem in _table:
        elem = remove_elem(source=elem, deletes=remove_elems)
        print(elem)
        if len(elem) == _len and unique_elem(elem):
            if skip_elems.count(elem[0]) != 0:
                pass
            else:
                elem.insert(0, elem[0])
            final.append(elem)
    return final


def complement(x, y):
    return x[:-len(y)] + y or x


def append_name(data):
    """
    Before:
        ['Name', 'Name', 'Price2018', 'Price2019']
        ['US', 'Price2018', 'Price2019']
        ['Non-US', 'Price2018', 'Price2019']
    After:
        ['Name', 'Name', 'Price2018', 'Price2019']
        ['Name', 'US', 'Price2018', 'Price2019']
        ['Name', 'Non-US', 'Price2018', 'Price2019']
    :param data:
    :return:
    """
    return list(itertools.accumulate(data, complement))


def remove_title(data):
    return [o for o in data if o[0] != o[1]]


def remove_column(_data: list[str], num_columns: list[int]):
    for num_column in num_columns:
        _data.pop(num_column)
    return _data

companies = ['Pfizer', 'Bristol']

path_to_pdf = "../Pdf_Storage/FinPfizer-19.pdf"


data = parse_pdf(file=path_to_pdf)
data = get_table(_result=data, start=["Revenues—Selected Product Discussion"], end=["PRODUCT DEVELOPMENTS—BIOPHARMACEUTICAL"])
max_len = max_length(data)
cols_num = columns_to_delete(data)

t = 0

table_count = 0
table_indexs = []

data_info = []
data_set = []
for company in companies:
    if company in path_to_pdf:
        data_info.append(company)
        break
    else:
        data_info.append('-')
        break

for span in data:

    if '$' in span and '$' not in data_info:
        for cols in span:
            if '$' in cols:
                data_info.append(cols)
                break

    if span[0] in ['•']:
        data_set.append(span[1])

    elif '(MILLIONS OF DOLLARS)' in span[0] and t == 0:
        for cols in span:
            if '20' in cols:
                t += 1
        table_count = t

    elif span[0] in ['U.S.', 'International']:
        for i in span:
            if i == '$':
                span.remove('$')
        data_set.append(span[0:table_count+1])


    elif '(MILLIONS OF DOLLARS)' in span[0] and len(data_info) == 2:
        for cols in span:
            if '20' in cols:
                data_info.append(cols)

    # if '(MILLIONS OF DOLLARS)' in span[0] and table_count == 0:
    #     tables = []
    #     for cols in span:
    #         if cols in ['Total', 'Oper.']:
    #             table_count -= 1
    #             table_indexs.append(table_count)
    #     tables = table_indexs.reverse()
    #     print(table_indexs)

# data_set = [remove_column(_data=data_set, num_columns=[-1]) for o in data]

print('Информация о данных:\n',data_info)
print('Нужные данные:',*data_set, sep='\n')
