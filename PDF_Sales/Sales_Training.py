import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json
import Sales_Funcs as amf  # Импорт функции для обучения

# Модуль распознавания денег и продуктов из аннуал отчётов
# Рекомендую с самого начал ознакомиться с комментариями и описаниями фунции, т.к. есть риск потерять данные

# << Загрузка модели распознавания текста >>
# << Drug_Model обученная на этих данных модель >>
# nlp = spacy.load("en_core_web_md")
# nlp = spacy.load('Drug_Model1')

# << Создание разметки для обучения !!! ЗАПУСКАТЬ ТОЛЬКО КОГДА ЗНАЕТЕ ЧТО ДЕЛАТЬ !!! >>
# amf.create_json('Drug_Train3.json', 'Raw_Train_Data.txt', nlp)

# << Обучение модели !!! ЗАПУСКАТЬ ТОЛЬКО КОГДА ЗНАЕТЕ ЧТО ДЕЛАТЬ !!! >>
# TRAIN_DATA = amf.load_data("Drugs_names_test1.json")
# nlp = amf.train_spacy(TRAIN_DATA, 30)
# nlp.to_disk("Drugs_names1")

# <<Создание словаря для обученной модели>>


# Тексты для проверки модели
if __name__ == "__main__":
    nlp = spacy.load('Drugs_names1')
    texts = ['Yervoy 1,489 1,330 12 % U.S. 1,004 941 7 % Non-U.S. 485 389 25 %',
            'Abraxane 166 — N/A U.S. 122 — N/A Non-U.S. 44 — N/A',
            'Empliciti 357 247 45 % U.S. 246 164 50 % Non-U.S. 111 83 34 %',
            'Sustiva Franchise 729 1,065 1,252 (32) % (15) % U.S. 622 901 1,041 (31) % (13) % Non-U.S. 107 164 211 (35) % (22) %',
             '622 901 1,041 (31) % (13'
             ]

    for list in texts:
        sells = amf.text_labels(list, nlp)
        print(sells)
        # print(list)