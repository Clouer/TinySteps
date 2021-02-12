import random

from flask import Flask, render_template, abort

from data import days
from scripts import get_teacher, get_schedule, get_goals, all_goals, all_teachers

app = Flask(__name__)


@app.route("/")
def render_main():
    teacher_list = []
    for teacher in all_teachers():
        teacher_list.append(teacher['id'])
    random_teachers = []
    for i in random.sample(teacher_list, 6):
        random_teachers.append(all_teachers()[i])
    return render_template("index.html",
                           teachers=random_teachers)


@app.route("/all/")
def render_all_teachers():
    return render_template("all.html")


@app.route("/goals/<goal>/")
def render_goals(goal):
    teachers_sorted = []
    for teacher in all_teachers():
        if goal in teacher["goals"]:
            teachers_sorted.append(teacher)
    if goal not in all_goals():
        abort(404)
    return render_template("goal.html",
                           teachers=teachers_sorted)


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
                           goals=goals)


@app.route("/request/")
def render_request():
    return render_template("request.html")


@app.route("/request_done/")
def render_request_done():
    return render_template("request_done.html")


@app.route("/booking/<int:teacher_id>/<day>/<time>/")
def render_booking(teacher_id, day, time):
    current_teacher = get_teacher(teacher_id)
    if current_teacher is None:
        abort(404)
    return render_template("booking.html",
                           teacher_name=current_teacher["name"],
                           teacher_picture=current_teacher["picture"],
                           day=days[day],
                           time=f"{time}:00")


@app.route("/booking_done/")
def render_booking_done():
    return render_template("booking_done.html")


app.run(debug=True)
