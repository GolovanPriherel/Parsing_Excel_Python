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
    for names, instructions in starts_stops.items():
        excel_file = pd.read_excel(file_name, sheet_name=None, header=None) #header=instructions[1]-2

        for sheet_name, sheet_value in excel_file.items():
            # print(sheet_name, '----')
            # print(sheet_value)
            # print(sheet_value.shape)
            if (sheet_value.shape[0] - instructions[1] > 0):
                table_select = sheet_value.iloc[instructions[1]-1]
                # print(table_select)
                # if sheet_name == 'TABLE14':
                #     print(start, '\n', sheet_value)
                for start in list(table_select):
                    # print(start)
                    if start == instructions[0]:
                        table = sheet_value
                        columns_check = table.rename(columns=sheet_value.iloc[instructions[2]-1])
                        if (len(instructions[4]) == 0) or (instructions[4][0] in list(columns_check)):
                            table = table.rename(columns=sheet_value.iloc[instructions[2]-1]).drop(table.index[range(0, instructions[2])])#.fillna('*%*')
                            # print(table)
                            for tables_del in instructions[4]:
                                if tables_del in list(table):
                                    table = table.drop([tables_del], axis=1)

                            table = table.dropna(how='all')

                            sales_list = extract_tables(table)
                            return sales_list, names
    # print(type(excel_file))