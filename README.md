# Запуск WEB приложения
1. Скопировать репозитой 
   
   git clone https://github.com/diomaxer/git_version_control.git

2. Перейти в папку репозитория
   
   cd git_version_control
   
3. Запустить docker-compos
   
   docker-compose up --build


# Работа приложения
1) создание бд
2) создание таблиц с помощью миграций
3) запуск сервера FastApi на localhost, порт 5000
4) запуск скрипта обновления данных о репозиторих пользователей добавленных в бд (записи обновляются каждый день в 00:00)


# Тестовые данные
Чтобы добавить пользоватлей в бд, перейдите по ссылке, откроется свагер fastapi
   
   http://0.0.0.0:5000/docs

нажмите на вкладку POST или перейдите по ссылке

   http://0.0.0.0:5000/docs#/Users/add_user_v1_users_post
   
 далее нажмиете "try it out"
 
 вставьте json 
 
```json
      {
        "id": 2,
        "login": "defunkt",
        "name": "Chris Wanstrath"
      }
```

нажмите "execute"
