"""
Создать страницу, на которой будет форма для ввода имени и электронной почты,
при отправке которой будет создан cookie-файл с данными пользователя, а также
будет произведено перенаправление на страницу приветствия, где будет
отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую
будет удалён cookie-файл с данными пользователя и произведено перенаправление
на страницу ввода имени и электронной почты.
"""

from flask import Flask, render_template, request, make_response, \
    redirect

app = Flask(__name__)


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    name = request.cookies.get('name')
    email = request.cookies.get('email')
    context = {'name': name,
               'email': email
               }

    return render_template("index.html", **context)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response(redirect("index"))
        response.set_cookie("name", name)
        response.set_cookie("email", email)

        return response

    return render_template('login.html')



@app.route('/delcookie', methods=['GET', 'POST'])
def delcookie():
    if request.method == 'POST':
        response = make_response(redirect("login"))
        response.delete_cookie("name")
        response.delete_cookie("email")

        return response

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
