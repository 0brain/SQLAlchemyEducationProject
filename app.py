# pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)  # ввів "app" екземпляр програми
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # створив в конфігурації спеціальну константу 'SQLALCHEMY_DATABASE_URI', яка визначає вид СУБД, яка буде використовуватися на проекті

db = SQLAlchemy(app) # ввів екземпляр класу SQLAlchemy, через який якраз здійснюється робота з БД і якому передається посилання на поточну програму app.


class Users(db.Model): # ввів клас Users, який наслідується від класу Model. Клас Model є базовим і якраз він перетворює класс Users в модель таблиці для SQLAlchemy.
    # Поля таблиці прописуються як звичайні змінні, які посилаються на спеціальний клас Column. Цей клас якраз і вказує SQLAlchemy сприймати ці змінні як поля таблиці.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # В кінці опису класу йде функція __repr__, яка визначає спосіб відображення класу в консолі. З її допомогою ми будемо виводити клас у вигляді рядка формату: <Users ідентифікатор>
        return f"<users {self.id}>"

if __name__ == "__main__":
    app.run(debug=True) # запуск веб-сервера