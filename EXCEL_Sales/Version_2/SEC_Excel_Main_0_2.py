from EXCEL_Sales.Version_2 import SEC_Excel_Funs_0_2 as sf

if __name__ == "__main__":
    # Логика словаря с инструкциями стар_стоп: {"<Название компании><год екселя*>" : "<Старт поиска>",
    #                            <строка с искомым словом**>, <строка с названиями столбцов в таблице с данными**>, "<Стоп поиска>",
    #                            [<Лист столбцов, которые нужно удалить>]}
    # Когда будут найдены старты и стопы будут возвращены страницы
    # * Вводятся только новые случаи оформления екселей, если из года в год не меняется, то не писать
    # ** Указывать индексы как в экселе, т.е. без -1

    starts_stops = {
                    'Pfizer-2015': ['Revenues-Major Biopharmaceutical Products', 10, 13, 'PRODUCT', ['PRIMARY INDICATIONS', 'Business(a)']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2014': ['Revenues-Major Biopharmaceutical Products', 17, 22, 'PRODUCT', ['PRIMARY INDICATIONS']], # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2013': ['PRIMARY INDICATIONS', 12, 12, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2012': ['Revenues-Major Biopharmaceutical Products', 10, 16, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2010': ['Revenues-Major Biopharmaceutical Products', 10, 17, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2009': ['Revenues-Major Pharmaceutical Products', 10, 19, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2008': ['Revenues-Major Pharmaceutical Products', 15, 25, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2007': ['Revenues-Major Pharmaceutical Products', 10, 21, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2006': ['Revenues - Major Human Health Products', 10, 17, 'PRODUCT', ['PRIMARY INDICATIONS']],  # Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2004': ['Revenues - Major Human Health Products', 15, 19, 'PRODUCT', ['PRIMARY INDICATIONS']],  #Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2003': ['Revenues - Major Pharmaceutical Products', 10, 15, 'PRODUCT', []],  #Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    'Pfizer-2002': ['REVENUES - MAJOR HUMAN PHARMACEUTICAL PRODUCTS', 10, 15, 'PRODUCT', []]  #Придумать как удалять столбцы вида ЦЦ/ЦЦ
                    }

    # Нахождение таблицы с продажами из экселей с использованием словаря

    excel_file = '../../EXCEL_Storage/Pfizer/Pfizer-2020.xls'

    sales_list, names = sf.read_excel_files(excel_file, starts_stops)

    for sales in sales_list:
        print(sales)

    print('\n', names, '\n')

    # if names in excel_file:
    #     print('\nСловари совпали\n')
    # else:
    #     print('\n!!!СРАБОТАЛ ЧУЖОЙ СЛОВАРЬ, ВОЗМОЖНА ПОТЕРЯ ДАННЫХ!!!\n')

