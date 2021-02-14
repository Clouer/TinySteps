import json
import random

from data import goals


def all_teachers():
    with open("teachers.json", encoding="utf-8") as teachers_json:
        return json.load(teachers_json)


def all_goals():
    with open("goals.json", encoding="utf-8") as goals_json:
        return json.load(goals_json)


def get_teacher(teacher_id):
    for i in all_teachers():
        if i["id"] == teacher_id:
            return i


def shuffle_random_teachers():
    teachers = all_teachers()
    random.shuffle(teachers)
    return teachers


def get_goals(teacher_id):
    goals_dict = {}
    personal_goals = get_teacher(teacher_id)["goals"]
    for personal_goal in personal_goals:
        goals_dict[personal_goal] = goals[personal_goal]
    return goals_dict


def get_schedule(teacher_id):
    schedule = get_teacher(teacher_id)["free"]
    free_schedule = {}
    for day in schedule:
        free_schedule[day] = {}
        for time in schedule[day]:
            if schedule[day][time]:
                free_schedule[day][time] = True
    return free_schedule


def booking_successful(teacher, day, time, name, phone):
    with open("booking.json", encoding="utf-8") as f:
        current_booking = json.load(f)
    if str(teacher) not in current_booking:
        current_booking[str(teacher)] = {"mon": [], "tue": [], "wed": [], "thu": [], "fri": [], "sat": [], "sun": []}
        print("teacher not in")
    current_booking[str(teacher)][day].append({"time": time, "name": name, "phone": phone})
    with open("booking.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(current_booking))
    with open("teachers.json", encoding="utf-8") as f:
        current_teacher = json.load(f)
    for i in current_teacher:
        if i["id"] == int(teacher):
            i["free"][day][time] = False
    with open("teachers.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(current_teacher))


def request_successful(name, phone, goal, time):
    with open("request.json", encoding="utf-8") as f:
        current_requests = json.load(f)
    current_requests.append({"name": name, "phone": phone, "goal": goal, "time": time})
    with open("request.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(current_requests))
