import json

import data

with open("teachers.json", "w", encoding="utf-8") as teachers_json:
    teachers_json.write(json.dumps(data.teachers))

with open("goals.json", "w", encoding="utf-8") as goals_json:
    goals_json.write(json.dumps(data.goals))
