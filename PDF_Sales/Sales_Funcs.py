import spacy
import re
import json
import random

def text_labels(text, nlp):
    text = re.sub('Int’l.', 'Non-U.S.', text)
    text = re.sub('[**]{2}', '0%', text)
    text = re.sub(r'[$]\s', '$', text)
    text = re.sub(r'\s[%]', '%', text)

    doc = nlp(text)

    list = []

    for ent in doc.ents:
        if ent.label_ in ['MONEY', 'CARDINAL', 'PRODUCT', 'PERSON', 'ORG', 'QUANTITY', 'PERCENT']:
            list.append(ent)
            # list.append(ent.label_)
    return list

def create_json(file_name, raw_data, nlp):
    """
    Разметка сущностей
    Прога создаёт новый json файл с разметкой сущностей с помощью актуальной nlp из файлика с сырой датой
    :param file_name:
    :return:
    """
    with open(file_name, 'w+') as new_file:
        texts = open(raw_data, 'r', encoding='utf-8')
        list = []
        for text in texts:
            text = re.sub('Int’l.', 'Non-U.S.', text)
            text = re.sub('[**]{2}', '0%', text)
            text = re.sub(r'[$]\s', '$', text)
            text = re.sub(r'\s[%]', '%', text)
            text = re.sub(r'\s+', '\n', text)

            doc = nlp(text)

            results = []
            entities = []
            for ent in doc.ents:
                # if ent.label_ in ['MONEY', 'CARDINAL', 'PRODUCT', 'PERSON', 'ORG', 'QUANTITY']:
                #     entt = ent.text.replace('\n', '')
                #     list.append(entt)
                # print(ent.text, ent.label_)
                text = re.sub(r'\n', ' ', text)
                entities.append((ent.start_char, ent.end_char, ent.label_))

            if len(entities) > 0:
                results = [text, {"entities": entities}]
                list.append(results)

        json.dump(list, new_file, indent=1)
    new_file.close()

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def train_spacy(data, iterations):
    """
    Создаёт обученную модель на размеченной выборке по кол-ву итераций
    :param data:
    :param iterations:
    :return:
    """
    TRAIN_DATA = data
    nlp = spacy.blank("en")
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print ("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                            [text],
                            [annotations],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses
                )
            print (losses)
    return (nlp)