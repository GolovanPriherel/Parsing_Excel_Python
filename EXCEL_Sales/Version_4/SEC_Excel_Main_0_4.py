from EXCEL_Sales.Version_4 import SEC_Excel_Funs_0_4 as sf
from glob import glob
import pandas as pd

if __name__ == "__main__":
    # Логика словаря с инструкциями стар_стоп: {"<Название компании><год екселя*>" : "<Старт поиска>",
    #                            <строка с искомым словом**>, <строка с названиями столбцов в таблице с данными**>, "<Стоп поиска>",
    #                            [<Лист столбцов, которые нужно удалить>]}
    # Когда будут найдены старты и стопы будут возвращены страницы
    # * Вводятся только новые случаи оформления екселей, если из года в год не меняется, то не писать
    # ** Указывать индексы как в экселе, т.е. без -1

    PFIZER = {
        'Pfizer-2020': [['Revenues-Selected Product Discussion'],
                        ['Product'],
                        ['PRODUCT'],
                        ['Revenues', 'Operational Results Commentary']],

        'Pfizer-2016': [['Revenues-Major Products'],
                        ['PRODUCT'],
                        ['Alliance Revenues'],
                        ['PRIMARY INDICATIONS', 'Business(a)', '/']],

        'Pfizer-2006': [['Revenues-Major Biopharmaceutical Products', 'Revenues-Major Pharmaceutical Products'],
                        ['PRODUCT'],
                        ['Alliance Revenues'],
                        ['PRIMARY INDICATIONS', 'Business(a)', '/']],

        'Pfizer-2004': [['Revenues - Major Human Health Products'],
                        ['(MILLIONS OF DOLLARS)'],
                        ['Alliance Revenues'],
                        ['PRIMARY INDICATIONS', '/']],

        'Pfizer-2003': [['Revenues - Major Pharmaceutical Products'],
                        ['(MILLIONS OF DOLLARS)'],
                        ['Alliance Revenue'],
                        ['/']],

        'Pfizer-2002': [['REVENUES - MAJOR HUMAN PHARMACEUTICAL PRODUCTS'],
                        ['(MILLIONS OF DOLLARS)'],
                        ['Alliance Revenue'],
                        ['/']]}
    BRISTOL = {
        'Bristol-2003': [['Date Filed: Mar 28, 2003'],
                         ['Pharmaceuticals'],
                         [],
                         []],
        'Bristol-2000': [['Sales of selected products and product categories are as follows:'],
                        ['1999'],
                        [],
                        []],
    }
    GSK = {
        'GSK-2000': [['Revenues-Selected Product Discussion'],
                        ['Product'],
                        ['PRODUCT'],
                        ['Revenues', 'Operational Results Commentary']],
    }
    AMGEN = {
        'AMGEN-2003': [['Revenues', 'Product sales'],
                     ['Product sales:', 'Change'],
                     [''],
                     ['Change']],
    }

    Company_dict = {
        'Pfizer': PFIZER,
        'Bristol': BRISTOL,
        'Amgen': AMGEN
                    }

    # Нахождение таблицы с продажами из экселей с использованием словаря

    # excel_file = 'Bristol/Bristol-2003.xls'
    # excel_file = 'Pfizer/Pfizer-2015.xls'
    # excel_file = 'Amgen/Amgen-2011.xls'

    sales_list = pd.DataFrame()
    final_list = pd.DataFrame()

    directory = 'Amgen/*.xls'
    # directory = 'Pfizer/*.xls'

    for filename in glob(directory):
        for comp_names, comp_values in Company_dict.items():
            try:
                sales_list, names = sf.read_excel_files(filename, comp_values)
                lst = [filename]
                dfnames = pd.DataFrame(lst)
                final_list = pd.concat([final_list, dfnames, sales_list])
                print(final_list)
            except:
                # sales_list = pd.DataFrame()
                names = []

                # print(final_list)

    # print(final_list)

    final_list.to_csv('SalesAmgen.csv', sep=';', encoding='utf-8')

                # file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
                # file_writer.writerow([filename])
                # for sales in sales_list:
                #     file_writer.writerow([sales])

                # for sales in sales_list:
                #     print(sales)
                #
                # print('\n', names, '\n')

        # if names in excel_file:
        #     print('\nСловари совпали\n')
        # else:
        #     print('\n!!!СРАБОТАЛ ЧУЖОЙ СЛОВАРЬ, ВОЗМОЖНА ПОТЕРЯ ДАННЫХ!!!\n')