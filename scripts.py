import json

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
