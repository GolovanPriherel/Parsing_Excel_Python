import re
import spacy
import csv
import json
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import Sales_Funcs as amf
# <<Просто файл с разными функциями для модуля распознавания>>

# <Создание переносов строк>
def add_spaces_from(file):
    with open(file, 'r') as f:
        new_file = open('../NLP_Train_materials/Raw_Train_Data2.txt', 'w')
        for line in f:
            new_text = re.sub('\sU.S.', '\nU.S.', line)
            new_text = re.sub('\sNon-U.S.', '\nNon-U.S.', new_text)
            new_text = re.sub('\sInt’l.', '\nNon-U.S.', new_text)
            print(new_text)
            new_file.write(new_text)
        new_file.close()

# <Создание списка продуктов>
def find_drugs_names(file):
    drugs = []
    with open(file, 'r') as f:
        csv_file = csv.reader(f, delimiter=';')
        for text in csv_file:
            drugs.append(text[0])
        drugs = set(drugs)
        return drugs

def create_training_data(list, type):
    data = list
    patterns = []
    for item in data:
        pattern = {
                    "label": type,
                    "pattern": item
                    }
        patterns.append(pattern)
    return (patterns)

def generate_rules(patterns):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    nlp.to_disk("Drugs_names")

def create_json_products(file_name, raw_data):
    with open(file_name, 'w+') as new_file:
        list = []
        for text in raw_data:
            results = []
            entities = []
            entities.append((0, len(text), 'PRODUCT'))

            if len(entities) > 0:
                results = [text, {"entities": entities}]
                list.append(results)

        json.dump(list, new_file, indent=1)
    new_file.close()

# drugs_names = find_drugs_names('Инфоид по драганским.csv')
# create_json_products('Drugs_names_test1.json', drugs_names)

# patterns = create_training_data(drugs_names, 'PRODUCT')
# generate_rules(patterns)