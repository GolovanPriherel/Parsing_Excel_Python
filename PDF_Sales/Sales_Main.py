import Sales_Parcing as amp
import spacy

def annual_module(path_to_pdf, spacy_model, start_stops):
    """
    Находит таблицы с продажами продуктов из аннуал отчётов и извлекает их них продукты и их региональные продажи
    :param path_to_pdf:
    :param spacy_model:
    :return:
    """
    for key, value in start_stops.items():
        sells_raw = amp.create_tables(path_to_pdf, value[0], value[1])

        # print(sells_raw)

        if sells_raw != None:
            break

    if sells_raw == None:
        print('No pages found')
        return sells_raw

    nlp = spacy.load(spacy_model)
    sells_list = amp.prepering_data(sells_raw)

    final_sells = amp.spacy_prepering_data(sells_list, nlp)  # Изменить тип вывода
    return final_sells

# Для тестов
if __name__ == "__main__":
    start_stops = {'Bristol1': ["Product Revenues", 'Total Revenues'],
                   'Bristol2': ["Product\nRevenues", 'Total Revenues'],
                   'GSK': ['Pharmaceutical turnover by therapeutic area 2019', 'Pharmaceuticals'],
                   'Pfizer': ['Revenues—Selected Product Discussion',
                              '2020 Form 10-K'],
                   'Amgen': ['Results\nProducts', 'Other\nOther']}

    # pdf = "Pdf_Storage/Amgen-20.pdf"
    # pdf = "Pdf_Storage/Pfizer-2020.pdf"
    # pdf = "Pdf_Storage/GSK-2020.pdf"
    pdf = "Pdf_Storage/Bristol-19.pdf"
    final_sells = annual_module(pdf, 'Drug_Model1', start_stops)
    for sell in final_sells:
        print(sell)