from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegistrationForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    email = StringField("Эл. почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль",
                             validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField("Подтвердите пароль",
                                     validators=[DataRequired(),
                                                 EqualTo("password"),
                                                 Length(min=5)])

