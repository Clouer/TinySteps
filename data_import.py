import json

import data
from app import Goal, db, Teacher

for goal_abb, goal_name in data.goals.items():
    goal = Goal(name=goal_name, name_abb=goal_abb)
    db.session.add(goal)

for teacher in data.teachers:
    new_teacher = Teacher(
        name=teacher["name"],
        about=teacher["about"],
        rating=teacher["rating"],
        picture=teacher["picture"],
        price=teacher["price"],
        free=json.dumps(teacher["free"])
    )
    db.session.add(new_teacher)
    for goal in teacher["goals"]:
        db_goal = db.session.query(Goal).filter(Goal.name_abb == goal).first()
        new_teacher.goals.append(db_goal)

db.session.commit()
