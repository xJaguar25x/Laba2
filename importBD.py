# -*- coding: utf-8 -*-

print ('Vk Photos geo location')

# загрузим базу данных с файла

# Считываем из БД данные
text = open('bd_V1.0.dat', 'r').read()
# Декодируем из utf8 в unicode - из внешней в рабочую
text = text.decode('utf-8')
# введем переменную и запишем туда весь файл БД
js_code = text
# Кодируем тест из unicode в utf8 - из рабочей во внешнюю
text = text.encode('utf-8')
# Закрываем файл БД
f = open('bd_V1.0.dat')
f.close()

# Считываем из файла-шаблона html данные
html = open('mapV1.2.html', 'r').read()
# Декодируем из utf8 в unicode - из внешней в рабочую
html = html.decode('utf-8')
# Заменяем placeholder на сгенерированный код
html = html.replace('/* PLACEHOLDER */', js_code)
# Кодируем тест из unicode в utf8 - из рабочей во внешнюю
html = html.encode('utf-8')
# Записываем данны в новый файл
f = open('VKPhotosGeoLocationV2.2.html', 'w')
f.write(html)
f.close()