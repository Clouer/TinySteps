import json
from pprint import pprint
import random

from data import goals
from scripts import get_teacher, all_teachers, get_schedule, request_successful

"""
booking = {}
teacher_id = 2
if teacher_id not in booking:
    booking[teacher_id] = {"mon": [], "tue": [], "wed": [], "thu": [], "fri": [], "sat": [], "sun": []}
pprint(booking)
booking[2]["mon"].append({"time": "12:00", "name": "Aloha", "phone": 123213})
booking[2]["mon"].append({"time": "14:00", "name": "Asdasd", "phone": 123})
pprint(booking)
"""

with open("booking.json", encoding="utf-8") as f:
    pprint(json.load(f))

with open("request.json", encoding="utf-8") as f:
    pprint(json.load(f))
