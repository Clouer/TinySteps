from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField, SelectField
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    clientName = StringField('Имя', [InputRequired(message='Пожалуйста, введите имя')])
    clientPhone = StringField('Телефон', [
        InputRequired(message='Пожалуйста, введите телефон'),
        Length(max=15, message="Максимальная длина телефона: 15 символов")])
    clientWeekday = HiddenField('День недели')
    clientTime = HiddenField('Время')
    clientTeacher = HiddenField('ID учителя')
    url = HiddenField('Current URL')


class RequestForm(FlaskForm):
    goal = RadioField("Цели", [InputRequired(message="Нужно выбрать цель")],
                      choices=[
                          ("travel", "Для путешествий"),
                          ("study", "Для учебы"),
                          ("work", "Для работы"),
                          ("relocate", "Для переезда"),
                          ("programming", "Для программирования")])
    time = RadioField("Сколько времени есть", [InputRequired(message="Нужно выбрать время")],
                      choices=[
                          ("1-2", "1-2 часа в неделю"),
                          ("3-5", "3-5 часов в неделю"),
                          ("5-7", "5-7 часов в неделю"),
                          ("7-10", "7-10 часов в неделю")])
    clientName = StringField('Имя', [InputRequired(message='Пожалуйста, введите имя')])
    clientPhone = StringField('Телефон', [
        InputRequired(message='Пожалуйста, введите телефон'),
        Length(max=15, message="Максимальная длина телефона: 15 символов")])


class SelectForm(FlaskForm):
    order = SelectField("Порядок сортировки",
                        choices=[
                            ("random", "В случайном порядке"),
                            ("rating", "Сначала лучшие по рейтингу"),
                            ("expensive", "Сначала дорогие"),
                            ("cheap", "Сначала недорогие")],
                        default="random")
