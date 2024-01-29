"""
Создать форму для регистрации пользователей на сайте. Форма должна содержать
поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных, а пароль должен
быть зашифрован.
"""

from flask_wtf.csrf import CSRFProtect
from homework_3.forms import RegistrationForm
from flask import Flask, render_template, redirect, url_for
from homework_3.models import db, User
from hashlib import sha256

app = Flask(__name__)
app.config[
    'SECRET_KEY'] = b'4ccc952703b8f4285eff644cf891487561ef0c2bbe8a2e0d9a44c94bac2d4747'
csrf = CSRFProtect(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/antonnovoselov/Desktop/' \
                                 'Flask/homework_3/instance/test.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route("/")
def index():
    return "Hi"


@app.route("/success/")
def success():
    return render_template("success.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    password=sha256(
                        form.password.data.encode(
                            encoding="utf-8")).hexdigest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("success"))


    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
