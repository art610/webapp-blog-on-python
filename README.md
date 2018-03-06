# webapp-blog-on-python  

Веб-приложение на Python, virtualenv, Wagtail (Django), Gunicorn (WSGI HTTP Server), PostgreSQL (pip psycopg2).
С примером веб-приложения на Wagtail можно ознакомиться [по ссылке.](http://forpology.ru/)

Для установки веб-приложения на Linux Debian из данного репозитория можно воспользоваться данной инструкцией:
1. Обновить зависимости и пакеты:
```
sudo apt-get update
yes | sudo apt-get dist-upgrade
```
2. Проверить доступные версии Python и при необходимости установить Python3:
```
python -V    # проверка версии python
python3 -V    # проверка версии python3
yes | sudo apt-get install python3    # установка python3, если отсутствует
```
3. Установить дополнительные утилиты python/pip:
```
yes | sudo apt-get install python3-setuptools python3-dev   # установка easy_install и python3-dev, если отсутствуют
sudo easy_install pip    # установка pip, если отсутствует
pip -V    # просмотр версии pip
sudo pip install --upgrade pip    # обновление pip при необходимости
```
4. Установить дополнительных библиотек:
```
yes | sudo apt-get install libtiff5-dev libjpeg9-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk gcc libc-dev
```
5. Установка и активация виртуального окружения:
```
sudo pip3 install virtualenv
sudo virtualenv /opt/artenv
cd /opt/artenv
source bin/activate 
```
Должно появится приглашение на подобие следующего: 
```
(myenv) art@local.develop.server:/opt/artenv$
```
6. Установка Wagtail и Gunicorn:
```
sudo pip3 install wagtail gunicorn
wagtail start artblog   # создание каркаса нашего приложения
```
7. Получить файлы, скачав их из данного репозитория, например, с помощью командной строки и следующей команды:
```
yes | sudo apt-get install git   # установка git

git clone https://github.com/lnovus/webapp-blog-on-python.git   # получение файлов
```
8. Заменить файлы в директории /opt/artenv/artblog файлами из репозитория (при скачивании находятся внутри webapp-blog-on-python/;
9. Перейти в основную папку проекта /opt/artenv/artblog и установить зависимости:
```
sudo pip install -r requirements.txt
```
10. Установить и настроить базу данных проекта (PostgreSQL):
```
sudo apt-get install libpq-dev postgresql postgresql-contrib
ps -ef | grep postgre    # проверим работу базы данных
# стандартный порт 5432
sudo pip install psycopg2   # установим утилиту для взаимодействия нашего приложения с базой данных
sudo su - postgres    # заходим под стандартным пользователем postgresql
psql    # запускаем консольную утилиту для связи с базой данных
# вводим запрос для создания базы данных и пользователя
CREATE DATABASE <dbname> with encoding='UNICODE';
CREATE USER <username> with password '<dbpassword>';
GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
# выходим из psql и завершаем сеанс пользователя postgres
\q
exit
# проверяем, что мы всё еще в виртуальной среде
# подключаем наше приложение к базе данных
sudo nano /opt/artenv/artblog/artblog/settings/base.py
# ищем запись DATABASES, и вносим указанные ранее значения
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': '<dbname>',
'USER': '<username>',
'PASSWORD': '<dbpassword>',
'HOST': 'localhost',
'PORT': '',
}
}
# при необходимости в том же файле можно установить русский язык
LANGUAGE_CODE = 'ru-ru'
# после чего закрываем редактор, сохраняя изменения: нажимаем ctrl+x, вводим y, нажимаем enter
```
11. Изменим первую строку в файле manage.py для того, чтобы она указывала на python в нашем виртуальном окружении и выполним миграцию:
```
sudo nano /opt/artenv/artblog/manage.py   # откроем в редакторе nano необходимый файл
# установим в первой строке запись, указывающую на python в виртуальном окружении, например, так #!/opt/artenv/bin/python
cd /opt/artenv/artblog    # перейдем в папку с нашим проектом
sudo python manage.py migrate   # выполним миграцию
# если появилась ошибка, что не установлен модуль django, то пробуем следующую команду, связанную с вашей версией python, например, в случае python3.6:
sudo python3.6 manage.py migrate  # далее используем вместо python нашу версию python3.x
```
12. Создаем профиль администратора и запускаем наше приложение:
```
cd /opt/artenv/artblog    # переходим в директорию нашего проекта
sudo python manage.py createsuperuser   # создаем администратора нашего приложения, вводим логин, email, пароль
deactivate    # отключим наше виртуальное окружение
python3.x manage.py runserver 0.0.0.0:8000    # запускаем приложение на 8000 порту для проверки и отладки
# если есть запрос на измнение ALLOWED_HOSTS, то делаем следующее
# добавляем наш хост в соответствующий пункт в settings.py
sudo nano /usr/local/lib/python3.x/dist-packages/django/conf/global_settings.py  # в качестве примера
# добавляем наши хосты в ALLOWED_HOSTS = ['localhost','127.0.0.1','domain.com'] и т.п.
python3.x manage.py runserver 0.0.0.0:80    # запускаем наше приложение на 80-м порту
```
13. Если мы работаем на сервере, например, через ssh клиент (PuTTY или другой), то возможно нам понадобится запустить приложение через nohup с установкой процесса в качестве фонового (в конце команды &), чтобы веб-приложение продолжило свою работу после закрытия ssh-клиента:
```
cd /opt/artenv/artblog    # переходим в директорию нашего проекта
nohup sudo python3.x manage.py runserver 0.0.0.0:80 &   # запускаем приложение в виде фонового процесса (задания)
jobs -p   # используем для просмотра наших заданий и их PID
ps -ef    # также можно просмотреть все процессы (если мы перелогинились до этого)
sudo kill PID   # для отключения нашего приложения используем данную команду  (PID находим при помощи команд, указанных выше
```
14. Для удобной работы в консоли Linux Debian возможно понадобятся следующие команды:
```
history   # история введенных нами команд (зависит от пользователя, под которым мы находимся)
!x    # x - номер команды из истории, позволяет выполнить определенную команду, введенную ранее
!!    # выполнить предыдущую команду
sudo !!   # выполнить предыдущую команду от имени администратора
```
15. Заметки по работе с Linux Debian можно также найти на GitBook [по данной ссылке.](https://lnovus.gitbooks.io/linux-debian-short-manual)

-----------
### Полезные ссылки: ###
* [Python3 | Docs](https://docs.python.org/3/)
* [PostgreSQL | Docs](https://www.postgresql.org/docs/9.6/static/index.html)
* [Python Package Index | pip](https://pypi.python.org/pypi)
* [Django | Docs](https://docs.djangoproject.com/en/1.11/contents/)
* [Wagtail CMS | Docs](http://docs.wagtail.io/en/v1.13.1/)
* [Markdown 2.6.11 | Python implementation of Markdown](https://pypi.python.org/pypi/Markdown)
* [Django-el-pagination | Django pagination tools](https://pypi.python.org/pypi/django-el-pagination/)
* [Django-taggit | Reusable Django application for simple tagging](https://pypi.python.org/pypi/django-taggit/)
* [GitHub Guides | Mastering Markdown](https://guides.github.com/features/mastering-markdown/)


