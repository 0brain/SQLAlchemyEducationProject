# pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)  # ввів "app" екземпляр програми
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # створив в конфігурації спеціальну константу 'SQLALCHEMY_DATABASE_URI', яка визначає вид СУБД, яка буде використовуватися на проекті

db = SQLAlchemy(app) # ввів екземпляр класу SQLAlchemy, через який якраз здійснюється робота з БД і якому передається посилання на поточну програму app.

if __name__ == "__main__":
    app.run(debug=True) # запуск веб-сервера