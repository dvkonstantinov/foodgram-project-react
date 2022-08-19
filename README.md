# Foogram - продуктовый помощник

## Описание проекта
Проект Foogram служит для закрепления навыков, полученных в ходе обучения в 
Яндекс Практикуме

## Стек
- ![workflow](https://github.com/dvkonstantinov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django rest framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Docker hub](https://hub.docker.com/)
- [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html)
- [Gunicorn](https://gunicorn.org/)
- [Nginx](https://www.nginx.com/)
- [Ubuntu](https://ubuntu.com/)
- [GitHub Actions](https://github.com/features/actions)


## Автоматизация всего и вся
За основу взят репозиторий https://github.com/dvkonstantinov/api_yamdb
К нему прикручена автоматизация:
- Тестирования pytest. Тесты находятся в каталоге /tests/
- Создание docker-образа и пуш этого образа на https://hub.docker.com/
- Разворачивание проекта на сервере (деплой) в случае успешного прохождения 
  тестов и пуш проекта в master-ветку.
  
## Разворачивание образа локально (Windows)
Предполагается наличие docker на локальной машине.
1. Склонировать репозиторий
```sh
git clone git@github.com:dvkonstantinov/foodgram-project-react.git
```
2. В склонированном репозитории перейти в каталог infra
```sh
cd infra
```
3. В файле nginx.conf изменить значение параметра server_name на 127.0.0.1
4. Создать файл с переменными окружения .env со следующим содержимым:
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<Название базы данных>
POSTGRES_USER=<Логин пользователя базы данных>
POSTGRES_PASSWORD=<Пароль базы данных>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<Секретный ключ из файла setting.py>
```
5. Запустить установку из файла docker-compose. Ключ -d для того чтобы 
   работать в фоне.
```sh
sudo docker-compose up -d
```
6. Сделать миграции в базе данных
```sh
sudo docker-compose exec backend python manage.py migrate
```
7. Создать суперпользователя
```sh
sudo docker-compose exec backend python manage.py createsuperuser
```
8. Заполнить базу данных подготовленными тегами и ингредиентами из csv файлов
```sh
sudo docker-compose exec backend python manage.py fill_tags
sudo docker-compose exec backend python manage.py fill_ingredients
```
9. Скопировать файлы статики
```sh
sudo docker-compose exec backend python manage.py collectstatic
```

10. Готово. В браузере открыть адрес http://127.0.0.1/

## Разворачивание проекта на сервере.
Подразумевается готовы настроенный личный или vps сервер с установленным 
docker, docker-compose, docker.io, настроенным firewall-ом и с доступом по 
ssh ключу.
1. Нажать кнопку fork, тем самым продублировать себе этот репозиторий.
2. Выполнить git clone <ваш_репозиторий> к себе на локальную машину
3. В django файле settings.py добавить в ALLOWED_HOSTS ip 
   адрес или домен вашего сервера и CSRF_TRUSTED_ORIGINS формата 
   http://<ваш_домен>
4. В файле /infra/nginx.conf в server_name добавить ip 
   адрес или домен вашего сервера
5. Скопировать файл docker-compose.yml в 
   home/<ваш_username>/foodgram/docker-compose.yml, а файл default.conf - в 
   home/<ваш_username>/nginx/default.conf
   
```sh
scp docker-compose.yml <имя_пользователя>@<ip_адрес_сервера>:/home/<имя_пользователя>/foodgram
scp nginx.conf <имя_пользователя>@<ip_адрес_сервера>:/home/<имя_пользователя>/foodgram
```
6. Прописать в настройках репозитория гитхаба secrets/actions. Они 
   преведены ниже в формате <name=value>. Подробнее их можно посмотреть в файле foodgram_workflow.yml.
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<Название базы данных>
POSTGRES_USER=<Логин пользователя базы данных>
POSTGRES_PASSWORD=<Пароль базы данных>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<Секретный ключ из файла setting.py>
DOCKER_PASSWORD=<Логин на сайте docker>
DOCKER_USERNAME=<Пароль на сайте docker>
HOST=<IP вашего сервера>
USER=<имя пользователя на сервере>
SSH_KEY=<Секретная часть ключа для доступа на сервер>
TELEGRAM_TO=<Ваш id в телеграме>
TELEGRAM_TOKEN=<Token телеграм бота>
```
8. Закоммитить и запушить на гитбах измененный код
9. Перейти во вкладку actions вашего репозитория и посмотреть правильность 
   работы workflow
10. Увидеть у себя в телеграме сообщение что все прошло успешно.
    
11. Далее зайти на сервер по ssh, убедиться что контейнеры подняты и работают
```sh
sudo docker container ls
```
12. Если все хорошо, то сделать миграции в базе данных
```sh
sudo docker-compose exec backend python manage.py migrate
```
13. Создать суперпользователя
```sh
sudo docker-compose exec backend python manage.py createsuperuser
```
14. Заполнить базу данных подготовленными тегами и ингредиентами из csv файлов
```sh
sudo docker-compose exec backend python manage.py fill_tags
sudo docker-compose exec backend python manage.py fill_ingredients
```
15. Скопировать файлы статики
```sh
sudo docker-compose exec backend python manage.py collectstatic
```
16. Заходить на сайт по адресу домена, который вы указали в nginx.conf

## Пример работающего сайта:
Главная страница - http://foodgram.dvkonstantinov.ru/
Страница админки - http://foodgram.dvkonstantinov.ru/admin/
Тестовые пользователи:
121demon@mail.ru:123 - суперпользователь
122demon@mail.ru:123qwe
123demon@mail.ru:123qwe
Сайт размещен на выданном сервере яндекса. Подписка со временем закончится 
и сайт перестанет работать.

## Подробная документация по API
Подробная документация по, по которой делался проект, размещена тут:
[http://foodgram.dvkonstantinov.ru/api/docs/](http://foodgram.dvkonstantinov.ru/api/docs/)
## Автор
dvkonstantinov
telegram: https://t.me/Dvkonstantinov

