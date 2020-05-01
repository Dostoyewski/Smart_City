#pip install reportlab

import requests as rq
import cv2
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

tok = '3a6c2d8a3a6c2d8a3a6c2d8a903a1da3d333a6c3a6c2d8a64c6cbd3fc1b20befe10ac47'
# Функция получает данные о пользователе по id и возвращвет словарь с информацией о пользователе
def request(id, token):
    pointer = "https://api.vk.com/method/users.get?user_id=" + str(id) + "&fields=bdate,sex,universities,schools,\
    interests,music,movies,tv,books,career,games,photo_400_orig,city&access_token=" + token + "&v=5.52"
    d1 = rq.get(pointer)
    return d1.json()['response'][0]

# Функция парсит словарь полученный из функции request
def parse_data(data):
    PERSON = {'ID': data['id'], 'first_name': data['first_name'], 'last_name': str(data['last_name']), 'sex':data['sex']}
    if 'photo_400_orig' in data:
        PERSON['photo'] = data['photo_400_orig']
    if 'bdate' in data:
        PERSON['birthday'] =  str(data['bdate'])
    if 'city' in data:
        PERSON['residence'] = str(data['city'].get('title'))
    schools = []
    univer = []
    work = []
    if 'schools' in data:
        for i in data['schools']:
            schools.append(str(i.get('name')) + ' : ' + str(i.get('year_from')) + '-' + str(i.get('year_to')))
    if 'universities' in data:
        for i in data['universities']:
            univer.append(str(i.get('name')) + ', ' + str(i.get('faculty_name')) + ', ' + str(i.get('chair_name')) + ', ' + str(i.get('year_from')) + '-' + str(i.get('year_to')))
    if 'career' in data:
        for i in data['career']:
            work.append(str(i.get('city')) + ', ' + str(i.get('company')) + ', ' + str(i.get('position')) + ', ' +  str(i.get('from')) + '-' + str(i.get('until')))
    intr ={}
    if 'interests' in data:
        intr['interest'] = str(data['interests'])

    if 'music' in data:
        intr['music'] = str(data['music'])
    
    if 'movies' in data:
        intr['movies'] = str(data['movies'])

    if 'tv' in data:
        intr['tv'] = str(data['tv'])
    
    if 'games' in data:
        intr['games'] = str(data['games'])
    
    PERSON.update({'school': schools, 'universite' : univer, 'work': work, 'hobbies': intr})

    return PERSON

# Скачивает фото по ссылке
def load_photo(url):
    obj = rq.get(url)
    name = "img.jpg" # МОжешь прописать свой каталог
    out = open(name, "wb")
    out.write(obj.content)
    out.close()
    img = cv2.imread(name)
    return img

# Фуекция создает список из id пользователей группы с groupid
def get_ids_group(groupid, token):
    pointer = "https://api.vk.com/method/groups.getMembers?group_id=" + str(groupid) + "&access_token=" + token + "&v=5.52"
    gr = rq.get(pointer)
    print(gr.json())
    users_ids = gr.json()['response'].get('items')
    
    return users_ids

# Функция создает из данных о пользователи анкету в формате PDF
def make_pdf_profile(data):
    fn = 'ID_' + str(data['ID']) + '.pdf'
    c = canvas.Canvas(fn) # МОжешь прописать свой каталог
    
    pdfmetrics.registerFont(TTFont('DJVU', 'DejaVuSansCondensed.ttf')) #Пропиши свой путь к каталогу
    c.setFont('DJVU', 8)
    if 'photo' in data:
        img = load_photo(data['photo'])
        c.drawImage(data['photo'], 10, 700, 5*cm, 5*cm)
    c.drawString(10,650,'Имя: ' + data['first_name'])
    c.drawString(10,630,'Фамилия: ' + data['last_name'])
    if data['sex'] ==  1:
        sex = 'женский'
    else:
        sex = 'мужской'
    c.drawString(10,610," Пол: " + sex)
    if 'residence' in data:
        c.drawString(10,590,'Адресс: ' + data['residence'])
    if 'birthday' in data:
        c.drawString(10,570,'Дата рождения: ' + data['birthday'])
    i = 0
    if 'school' in data:
        c.drawString(10,550, 'Школы: ')
        for sc in data['school']:
            c.drawString(10,530 - i, sc)
            i += 20
    if 'universite' in data:
        i += 20
        c.drawString(10,550 - i, 'Высшее образование: ')
        for un in data['universite']:
            c.drawString(10,530 - i, un)
            i += 20
    if 'work' in data:
        i += 20
        c.drawString(10,550-i, 'Места работы: ')
        for un in data['work']:
            c.drawString(10,530 - i, un)
            i += 20
    i += 20
    if  'hobbies' in data:
        i += 20
        c.drawString(10,550 - i, 'Увлечения: ')
        i += 20
        if 'interest' in data['hobbies']:
            c.drawString(10,550 - i, 'Интересы: ' + data['hobbies'].get('interest'))
            i += 20
        if 'music' in data['hobbies']:
            c.drawString(10,550 - i, 'Музыка: ' + data['hobbies'].get('music'))
            i += 20
        if 'movies' in data['hobbies']:
            c.drawString(10,550 - i, 'Фильмы: ' + data['hobbies'].get('movies'))
            i += 20
        if 'tv' in data['hobbies']:
            c.drawString(10,550 - i, 'Передачи: ' + data['hobbies'].get('tv'))
            i += 20
        if 'games' in data['hobbies']:
            c.drawString(10,550 - i, 'Игры: ' + data['hobbies'].get('games'))
            i += 20
    c.showPage()
    c.save()

# Данные в csv
def make_csv(data):
    d = pd.DataFrame(data)
    d.to_csv("frame.csv")
    print(d.head(10))
    return d

#ПРИМЕР :
ids = get_ids_group("theormech", tok) # Получаем Id-пользователей сообщества ВШТМ
print(ids)

DATASET = [] # Данные пользователей
PHOTOS = [] # Фото пользователей
i = 0

for id in ids:
    user = parse_data(request(id, tok)) # получаем данные пользователей
    if 'photo' in user:
        PHOTOS.append(load_photo(user['photo']))
    else:
        PHOTOS.append("NONE")

    DATASET.append(user) #Добавляем в сиписок
    print(DATASET[i])
    i += 1
    if i >= 25: #Берем первые 25 а то долго грузится
       break

make_csv(DATASET)

for i in range(len(DATASET)):
    make_pdf_profile(DATASET[i])














