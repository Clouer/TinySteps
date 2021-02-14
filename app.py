import os
import random

from flask import Flask, render_template, abort, request, redirect
from flask_wtf.csrf import CSRFProtect

from data import days, time_week
from forms import BookingForm, RequestForm, SelectForm
from scripts import get_teacher, get_schedule, get_goals, all_goals, all_teachers, booking_successful, \
    request_successful, shuffle_random_teachers

app = Flask(__name__)
csrf = CSRFProtect(app)

SECRET_KEY = os.urandom(43)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def render_main():
    teacher_list = []
    for teacher in all_teachers():
        teacher_list.append(teacher['id'])
    random_teachers = []
    for i in random.sample(teacher_list, 6):
        random_teachers.append(all_teachers()[i])
    return render_template("index.html",
                           teachers=random_teachers,
                           goals=all_goals(),
                           title="TINYSTEPS")


@app.route("/all/", methods=["GET", "POST"])
def render_all_teachers():
    form = SelectForm()
    if request.method == "POST":
        order = form.order.data
        if order == "random":
            return redirect("/all/")
        return render_template("all.html",
                               teachers=all_teachers(),
                               form=form,
                               order=order)
    return render_template("all.html",
                           teachers=shuffle_random_teachers(),
                           form=form,
                           title="Все преподаватели")


@app.route("/goals/<goal>/")
def render_goals(goal):
    teachers_sorted = []
    for teacher in all_teachers():
        if goal in teacher["goals"]:
            teachers_sorted.append(teacher)
    if goal not in all_goals():
        abort(404)
    return render_template("goal.html",
                           goal=all_goals()[goal],
                           teachers=teachers_sorted,
                           title=f"Преподаватели {all_goals()[goal]}")


@app.route("/profiles/<int:teacher_id>/")
def render_teacher(teacher_id):
    current_teacher = get_teacher(teacher_id)
    if current_teacher is None:
        abort(404)
    schedule = get_schedule(teacher_id)
    goals = get_goals(teacher_id)
    return render_template("profile.html",
                           name=current_teacher["name"],
                           id=teacher_id,
                           about=current_teacher["about"],
                           rating=current_teacher["rating"],
                           price=current_teacher["price"],
                           picture=current_teacher["picture"],
                           days=days,
                           schedule=schedule,
                           goals=goals,
                           title=current_teacher["name"])


@app.route("/request/")
def render_request():
    form = RequestForm()
    return render_template("request.html",
                           form=form,
                           title="Подбор преподавателя")


@app.route("/request_done/", methods=["GET", "POST"])
def render_request_done():
    if request.method == "GET":
        return redirect("/request/")
    form = RequestForm()
    if form.validate_on_submit():
        goal = form.goal.data
        time = form.time.data
        name = form.clientName.data
        phone = form.clientPhone.data
        request_successful(name, phone, goal, time)
        return render_template("request_done.html",
                               name=name,
                               phone=phone,
                               time=time_week[time],
                               goal=all_goals()[goal],
                               title="Запрос отправлен!")
    else:
        return render_template("request.html", form=form)


@app.route("/booking/<int:teacher_id>/<day>/<time>/")
def render_booking(teacher_id, day, time):
    current_teacher = get_teacher(teacher_id)
    try:
        current_teacher["free"][day][f"{time}:00"]
    except KeyError:
        abort(404)
    if current_teacher is None or not current_teacher["free"][day][f"{time}:00"]:
        abort(404)
    form = BookingForm()
    return render_template("booking.html",
                           teacher_name=current_teacher["name"],
                           teacher_id=teacher_id,
                           teacher_picture=current_teacher["picture"],
                           day_key=day,
                           day_value=days[day],
                           time=f"{time}:00",
                           form=form,
                           title="Запись на пробный урок")


@app.route("/booking_done/", methods=["POST", "GET"])
def render_booking_done():
    if request.method == "GET":
        return redirect("/")
    form = BookingForm()
    day = form.clientWeekday.data
    time = form.clientTime.data
    teacher = get_teacher(int(form.clientTeacher.data))
    name = form.clientName.data
    phone = form.clientPhone.data
    booking_successful(form.clientTeacher.data, day, time, name, phone)
    return render_template("booking_done.html",
                           day=days[day],
                           time=time,
                           teacher_picture=teacher["picture"],
                           name=name,
                           phone=phone,
                           title="Заявка успешно отправлена")


if __name__ == '__main__':
    app.run()
