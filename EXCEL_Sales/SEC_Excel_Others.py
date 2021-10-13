from dateutil.parser import parse
import datetime
import csv
import pandas as pd

# def create_drugs_dates(file):
#     drugs = []
#     with open(file, 'r') as f:
#         csv_file = csv.reader(f, delimiter=';')
#         # new_file = open('Drugs_Sells_Clean.csv', 'w')
#         for text in csv_file:
#             if datetime.datetime(text[4])
#             drugs.append(text[4])
#         drugs = set(drugs)
#         return drugs

def correct_time(date_to_change):
    new_date = parse(date_to_change)
    date_struct = str(new_date.date()).split('-')
    date_obj = datetime.datetime(int(date_struct[0]), int(date_struct[1]), int(date_struct[2]))
    new_date = date_obj.strftime('%m.%d.%Y').replace('/', '.')
    if int(date_struct[0]) < 1992:
        # print(int(date_struct[0]))
        return '01.01.1000'
    else:
        return new_date

    # date = str(date_def.date()).split('-')
    # date_obj = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    # final_date = date_obj.strftime('%m.%d.%Y').replace('/', '.')
    # date_to_change[1] = final_date
    # return date_to_change


if __name__ == '__main__':
    with open('../EXCEL_Storage/Drugs_Sells_2.csv') as drugs:
        with open('../EXCEL_Storage/Drugs_Dates.csv', 'w') as dd:
            writer = csv.writer(dd, delimiter=';')
            next(drugs)
            drug_sales = csv.reader(drugs, delimiter=';')
            drug_list = list(drug_sales)

            for lines in drug_list:
                # print(str(lines[4]))
                try:
                    new_date = correct_time(lines[4])
                except:
                    new_date = '01.01.1000'

                lines[4] = new_date

            writer.writerows(drug_list)

            # print(new_date)

        # print(df['Action Date'])

        # drugs_dates = create_drugs_dates('Drugs_Sells_2.csv')
        # print(drugs_dates)

        # date = correct_time('11-19-2021')