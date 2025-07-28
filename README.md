# Интернет-магазин на Django
python manage.py runserver - запуск веб-приложения. Ctrl+C - остановка сервера.

python manage.py createadmin - создание суперпользователя

python manage.py send_mailings - запуск рассылки через командную строку

python manage.py export_users --output=my_users.json - экспорт пользователей
приложения в файл json

python manage.py add_users - создание тестовых пользователей

ВАЖНО!!! Регистрация пользователя на сайте происходит через письмо с подтверждением, которое
отправляется на email пользователя. Если регистрируетесь под вымышленным email, в админке под
администратором поставьте у этого пользователя с вымышленным email галочку "Active", чтобы
можно было потом под ним авторизоваться на сайте.
## Описание:

Веб-приложение для рассылки писем списку пользователей.

## Требования к окружению:

Установите:
 - python 3.13.0
 - Poetry
 - Django
 - Pillow
 - python-dotenv
 - psycopg2 или psycopg2-binary
 - redis

## Установка:

1. Клонируйте репозиторий:
```
https://github.com/Bugrova-Irina/coursework_django_web/
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
```
poetry shell
```
```
poetry add django
```
```
poetry add Pillow
```
```
poetry add psycopg2
```
```
poetry add python-dotenv
```
```
poetry add redis
```

## Использование:

После запуска сервера перейдите по ссылке http://127.0.0.1:8000/.

## Тестирование:

Не реализовано

## Документация:

Нет дополнительной информации.

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)