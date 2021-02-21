import os
import random

from flask import Flask, render_template, abort, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.dialects.postgresql import JSON

from data import days, time_week
from forms import BookingForm, RequestForm, SelectForm
from scripts import get_teacher, get_schedule, get_goals, all_goals, all_teachers, booking_successful, \
    request_successful, shuffle_random_teachers

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)
SECRET_KEY = "SUPER_secret_KEY"
app.config['SECRET_KEY'] = SECRET_KEY

teachers_goals_associations = db.Table("teachers_goals",
                                       db.Column("teacher_id", db.Integer, db.ForeignKey("teachers.id")),
                                       db.Column("goal_id", db.Integer, db.ForeignKey("goals.id"))
                                       )

requests_goals_associations = db.Table("requests_goals",
                                       db.Column("request_id", db.Integer, db.ForeignKey("requests.id")),
                                       db.Column("goal_id", db.Integer, db.ForeignKey("goals.id"))
                                       )


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(JSON)
    bookings = db.relationship("Booking", cascade="all,delete", back_populates="teacher")
    goals = db.relationship("Goal", secondary=teachers_goals_associations, back_populates="teachers")


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    teacher = db.relationship("Teacher", back_populates="bookings")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_abb = db.Column(db.String(100), nullable=False)
    teachers = db.relationship("Teacher", secondary=teachers_goals_associations, back_populates="goals")
    requests = db.relationship("Request", secondary=requests_goals_associations, back_populates="goals")


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    goals = db.relationship("Goal", secondary=requests_goals_associations, back_populates="requests")


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
    app.run(debug=True)
