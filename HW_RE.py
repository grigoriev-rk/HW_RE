import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)
#type(contacts_list)
# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

pattern1 = r'''(^[А-Я][а-я]*)[,\s]*([А-Я][а-я]*)[,\s]*([А-Я]*[а-я]*)[,\s]*
              ([А-ЯЁа-яё]*)[,\s]*([А-ЯЁа-яё\s–c]*)[,\s]*(\+7|8)*[\s\)\(-]*
              (\d{3})?[\s\)\(-]*(\d{3})?[\s\)\(-]*(\d{2})?[\s\)\(-]*
              (\d{2})?[\s\(\)доб\.]*(\d{4})?[\s\(\)доб\.,]*([A-Za-z.@0-9]*)'''

result1 = re.findall(pattern1, contacts_list)
pprint(result1)

substitution = r'+7(\7)\8-\9-\10' 
result2 = re.sub(pattern1, substitution, result1)
pprint(result2)


#TODO 2: сохраните получившиеся данные в другой файл
#код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8') as ff:
    datawriter = csv.writer(ff, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(result2)
