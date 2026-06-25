from faker import Faker
import random
from typing import Dict, List
fake = Faker()


def generate_student(student_id: int) -> Dict:
    return {
        "ID": student_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": random.randint(18, 80)
    }


def generate_students(n: int) -> List[Dict]:
    students = []

    for i in range(1, n + 1):
        students.append(generate_student(i))

    return students


print(generate_students(5))