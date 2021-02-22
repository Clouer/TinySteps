import json

import app as a


def all_teachers():
    return a.db.session.query(a.Teacher).all()


def all_goals():
    return a.db.session.query(a.Goal).all()


def get_teacher(teacher_id):
    return a.db.session.query(a.Teacher).get_or_404(teacher_id)


def get_goals(teacher_id):
    return a.db.session.query(a.Teacher).get(teacher_id).goals


def get_schedule(teacher_id):
    schedule = json.loads(a.db.session.query(a.Teacher).get(teacher_id).free)
    free_schedule = {}
    for day in schedule:
        free_schedule[day] = {}
        for time in schedule[day]:
            if schedule[day][time]:
                free_schedule[day][time] = True
    return free_schedule


def booking_successful(teacher, day, time, name, phone):
    schedule = get_schedule(teacher.id)
    schedule[day][time] = False
    teacher.free = json.dumps(schedule)
    booking = a.Booking(name=name, phone=phone, day=day, time=time, teacher=teacher)
    a.db.session.add(booking)
    a.db.session.commit()


def request_successful(name, phone, goal, time):
    new_request = a.Request(name=name, phone=phone, time=time)
    a.db.session.add(new_request)
    new_request.goals.append(goal)
    a.db.session.commit()
