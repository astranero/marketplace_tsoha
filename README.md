# AstraMarket - Find your way to the stars

<img src="https://images.unsplash.com/photo-1534447677768-be436bb09401?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1194&q=80" width="760"> 

Photo by Jeremy Bishop on Unsplash

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)


AstraMarket is web-application for selling and buying products.
* Registering as normal user can be done by clicking 'Sign Up' button. For registering as admin user you have to use flask commandline.
* Users can add products, edit products, and comment on them. User can also delete these.
* Users can also report unappropriate comments.
* Admins can hide these reported comments and also permanently ban users. 
* Banned users can't log in anymore.
* Users can like each others profiles.
* In marketplace products can be searched for with search bar. Category, condition and sorting order of the products can also be specified.

## Installation instruction

### Requirements

* Python version 3.8.1 or higher
* PostgreSQL database

### Configuration:

In the root folder of the application create `.env` file. 
In .env file set variable `SQLALCHEMY_DATABASE_URI` as path to postgresql database, and secret key to `SECRET_KEY` variable.
Also set variables `UPLOAD_FOLDER=src/static` and `FLASK_APP=src/app.py`

Example:
```
SECRET_KEY=Strong_secret_key
SQLALCHEMY_DATABASE_URI=postgresql://database_name:password@localhost/database_user
DB_HOST=localhost
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=password
UPLOAD_FOLDER=src/static
FLASK_APP=src/app.py
```

### Running the program

1. Install requirements from requirement.txt file with pip.
```
pip3 install -r requirement.txt
```
2. In root directory of application first activate venv.
```
Source venv/bin/activate
```
3. Now run flask.
```
flask run
```

To initiate database just run schema.py file.

## Host

This application can be accessed in heroku:

https://marketplacetsoha.herokuapp.com/login

To try admin functionalities use following credentials:
<br>
Username=admin
<br>
Password=admin

## What I learned & What application is lacking?

I learned how to use css, html and bootstrap in depth. I also tried to learn flask methods and extensions as much as possible. I learned to implement flask in my own ways, but at the risk of there being some security issues. I am not sure if post_injection of database methods with context_processor is safe yet, and have to find out more about that. I found post_injection useful in fetching information data to jinga.

I think report functionalities are lacking. In the future I would like to offer users possibility of reporting products and other users. Also I thought that encapsulation of python functions wasn't good enough. I want to put more thought into how to arrange methods into classes, and when its wise to use classes? Is it always needed?
