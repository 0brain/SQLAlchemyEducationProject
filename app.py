# pip install Flask-SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)  # ввів "app" екземпляр програми
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # створив в конфігурації спеціальну константу 'SQLALCHEMY_DATABASE_URI', яка визначає вид СУБД, яка буде використовуватися на проекті

db = SQLAlchemy(app) # ввів екземпляр класу SQLAlchemy, через який якраз здійснюється робота з БД і якому передається посилання на поточну програму app.


class Users(db.Model): # ввів клас Users, який наслідується від класу Model. Клас Model є базовим і якраз він перетворює класс Users в модель таблиці для SQLAlchemy.
    # Поля таблиці прописуються як звичайні змінні, які посилаються на спеціальний клас Column. Цей клас якраз і вказує SQLAlchemy сприймати ці змінні як поля таблиці.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False) # pr - змінна через яку буде встановлюватися зв'язок з таблицею Profiles по зовнішньому ключу user_id. Параметр backref вказує таблицю, до якої приєднувати записи з таблиці profiles. Останнє значення uselist = False вказує, що одному запису з users повинна відповідати один запис з profiles.

    def __repr__(self): # В кінці опису класу йде функція __repr__, яка визначає спосіб відображення класу в консолі. З її допомогою ми будемо виводити клас у вигляді рядка формату: <Users ідентифікатор>
        return f"<users {self.id}>"


class Profiles(db.Model):   # ввів клас Profiles, який теж наслідується від класу Model.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route("/")
def index():
    return render_template("index.html", title="Головна")

@app.route("/register", methods=("POST", "GET"))  # по адресу "/register" будемо отримувати дані по "POST" і "GET" запиту
def register(): # ввів функцію для опрацювання адресу "/register", яка буде відображати шаблон "register.html"
    if request.method == "POST": # перевіряємо, що дані прийши по пост запиту
        try:
            hash = generate_password_hash(request.form['psw'])  # з форми ми беремо пароль, який користувач ввів при реємтрації і генеруємо для нього хеш
            u = Users(email=request.form['email'], psw=hash)  # створюємо екземпляр класу Users і через параметри email і psw передаємо дані екземпляру класу Users. В результаті створюється об'єкт з даними по email і паролю, який і являє собою майбутню запис в таблиці users.
            db.session.add(u)  # щоб добавити сформований запис в таблицю відбувається звернення до спеціального об'єкту session - сесії БД і в неї додається запис за допомогою методу add. Як параметр цей метод приймає посилання на об'єкт класу Users.
            db.session.flush()  # виконується метод flush, який з сесії переміщує запис в таблицю. Дана таблиця все ще в памяті, тобто зміни не внесені.

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id) # Якщо помилок не виникає, то формується наступний екземпляр класу Profiles з набором даних з форми. Додатково береться значення u.id, яке сформувалося після методу flush при додаванні запису в таблицю users. Саме тому ми викликали метод flush.
            db.session.add(p)  # Далі, запис поміщається в сесію.
            db.session.commit() # І викликається метод commit, який вже фізично змінює файли БД і зберігає зміни в таблицях.
        except:
            db.session.rollback() # Якщо при додаванні в базу даних виникли помилки, то ми відкатуємо її до попереднього стану.
            print("Помилка додавання в БД") # І виводимо повідомлення про помилку.

        return redirect(url_for('index'))
    return render_template("register.html", title="Реєстрація")

if __name__ == "__main__":
    app.run(debug=True) # запуск веб-сервера