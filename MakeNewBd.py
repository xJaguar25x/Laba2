# -*- coding: utf-8 -*-
import vk
import time

print ('Vk Photos geo location')

# Авторизируем сессию с помощью acceess token
session = vk.Session('b26d05...6be6e')

# Или с помощью id приложения и данных авторизации пользователя
# session = vk.AuthSession('app id','login','pass')

# Создаем объект Api
api = vk.API(session)

# Запращиваем список всех друзей
friends = api.friends.get()  #[766013, 1007957, 2613990, 3201357,...]

print ('Количество пользователей: %s' % len(friends))
"""
print (friends) #[766013, 1007957, 2613990, 3201357,...]"""

# Получаем информацию о всех друзьях
# Создадим массив имен и айди
# Перебираем всех пользователей по id друзей, если есть заносим доп информацию пользователей
friends_info = api.users.get(user_ids=friends)
"""print friends_info""" #[{u'first_name': u'Frankie', u'last_name': u'\u0424\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0443\u043c', u'uid': 766013},...]

# Выведем информацию в удобном виде
for friend in friends_info:
    print ('ID: %s Name: %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))

# Список для хранения данных
geo_friends_info = []

# Получим геоданные всех фотографий каждого друга
# Цикл перебирающий всех друзей

for friend in friends_info:
  # if friend ['uid'] == 16196807: # Фильтр для 1 друга (тест)
    # Обрабатываем исключение для приватных альбомов/фото
    try:
        print(u'Получаем данные %s %s ID = %s' % (friend['last_name'], friend['first_name'], friend['uid']))
        # Получаем все альбомы пользователя, кроме служебных
        albums = api.photos.getAlbums(owner_id=friend['uid'])
        print ('\t...албомов %s...' % len(albums))
        # Цикл перебирающий все альбомы пользователя
        for album in albums:
            # получаем все фотографии из альбома
            photos = api.photos.get(owner_id=friend['uid'], album_id=album['aid'])
            print ('\t\t...обрабатываем фотографии альбома... aid=%s' % (album['aid']))
            # Цикл перебирающий все фото в альбоме
            for photo in photos:
                # Если в фото имеются геоданные, то добавим их в список geo_friends_info
                if 'lat' in photo and 'long' in photo:
                    geo_friends_info.append(
                        (photo['lat'], photo['long'], friend['first_name'], friend['last_name'], friend['uid']))
            print ('\t\t...найдено %s фото...' % len(photos))

            # Задержка между запросами photos.get
            time.sleep(0.5)


        # получаем все фотографии из альбома
        """photos_wall = api.photos.get(owner_id=friend['uid'], album_id=-7)
        print ('\t\t...обрабатываем фотографии альбома... aid=%s' % 'wall')
        # Цикл перебирающий все фото в альбоме
        for photo in photos:
            # Если в фото имеются геоданные, то добавим их в список geo_friends_info
            if 'lat' in photo and 'long' in photo:
                geo_friends_info.append((photo['lat'], photo['long'], friend['first_name'], friend['last_name'], friend['uid']))
        print ('\t\t...найдено %s фото...' % len(photos))"""

        # Задержка между запросами photos.get
       # time.sleep(0.5)
    except:
        pass
    # Задержка между запросами photos.getAlbums
    time.sleep(0.5)

print geo_friends_info

# Здесь будет храниться сгенерированный JAvaScript код
js_code = ""

# Введем переменную для указателей позже можно будет сделать в качестве указателя имена и юйди друзей
i = 0
# Проходим по всем геоданным и генерируем JS команду добавления маркера
for loc in geo_friends_info:
    i +=1
    if len(geo_friends_info) == i:
        js_code += '\n\t{\n\t lat: %s,\n\t lng: %s,\n\t name: "%s %s",\n\t friend_id: %s\n\t}' % (loc[0], loc[1], loc[2], loc[3], loc[4])
    else:
        js_code += '\n\t{\n\t lat: %s,\n\t lng: %s,\n\t name: "%s %s",\n\t friend_id: %s\n\t},' % (loc[0], loc[1], loc[2], loc[3], loc[4])


# Считываем из файла-шаблона html данные
html = open('mapV1.2.html', 'r').read()
# Декодируем из utf8 в unicode - из внешней в рабочую
html = html.decode('utf-8')
# Заменяем placeholder на сгенерированный код
html = html.replace('/* PLACEHOLDER */', js_code)
# Кодируем тест из unicode в utf8 - из рабочей во внешнюю
html = html.encode('utf-8')
# Записываем данны в новый файл
f = open('VKPhotosGeoLocationV2.1.html', 'w')
f.write(html)
f.close()

# создадим базу данных
text = js_code
# Кодируем тест из unicode в utf8 - из рабочей во внешнюю
text = text.encode('utf-8')
# Записываем данны в новый файл
f = open('bd_V1.0.dat', 'w')
f.write(text)
f.close()
