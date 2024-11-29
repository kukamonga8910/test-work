# Приложение, выводящее табличку автомобилей и позволяющее добавлять автомобили
### Стек
- nginx
- php
- mysql
### Клонирование репозитория
```
$ git clone https://github.com/AnastasiyaGapochkina01/simple_php_app.git /var/www/simple_app
$ cd /var/www/simple_app
```
### Создание БД
```
$ sudo mysql < simple_data.sql
```
### Конфигурация nginx
```
$ sudo cp simple_app /etc/nginx/sites-available/simple_app
$ sudo ln -s /etc/nginx/sites-available/simple_app /etc/nginx/sites-enabled
$ sudo nginx -t
$ sudo nginx -s reload
```
Результат работы:
по адресу машины должно открываться
![result](https://github.com/AnastasiyaGapochkina01/simple_php_app/blob/main/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202023-09-08%2013-46-33.png?raw=true)
