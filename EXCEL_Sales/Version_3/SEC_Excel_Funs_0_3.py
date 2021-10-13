import pandas as pd
import numpy as np
import re

def extract_tables(tables):
    result_list = []
    # for names, tables in excel_file.items():
    sells_table = tables.fillna('')
    sells_table = np.array(sells_table)
    # print(sells_table)
    for i in range(sells_table.shape[0]):
        result = ''
        for j in range(sells_table.shape[1]):
            if sells_table[i][j] != '':
                result += str(sells_table[i][j]) + ' '
                result = result.replace('.0 ', ' ')
                result = re.sub(r'\s(-?)0[.]0?(\d{1,2})', r' \1\2%', result)
                result = result.replace(' )', ')')
                result = result.replace('**', '0%')
                result = result.replace('-', '')
        result = result[0:-1]
        result_list.append(result)

    return result_list
    # for res in result_list:
    #     print(res)

def read_excel_files(file_name, starts_stops):

    sales_list = []
    start_pos = False

    for names, instructions in starts_stops.items():

        excel_file = pd.read_excel(file_name, sheet_name=None, header=None) #header=instructions[1]-2

        for sheet_name, sheet_value in excel_file.items():
            table = sheet_value
            # print(sheet_name, '----')
            # print(sheet_value)
            # print(sheet_value.shape)
            for line in range(0, sheet_value.shape[0]):
                line_check = sheet_value.iloc[line]
                # print(list(line_check))
                for columns in list(line_check):
                    if columns in instructions[0]:
                        # print(columns)
                        start_pos = True
                    elif columns in instructions[1] and start_pos is True:
                        # print(list(line_check))
                        # print(sheet_name)

                        table = table.rename(columns=sheet_value.iloc[line])\
                            .drop(table.index[range(0, line+1)])\
                            .dropna(axis='columns', how='all')

                        for tables_del in instructions[3]:
                            for columns_del in list(table):
                                # print(type(list(table)))
                                if str(tables_del) in str(columns_del):
                                    # print(type(columns_del))
                                    table = table.drop([columns_del], axis=1)

                        table = table.dropna(how='all')
                        # print(table)

                        sales_list = extract_tables(table)
                        return sales_list, names