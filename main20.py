# home word 1

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: ({self.name}, {self.age})"


p1 = Person("Otar", 35)


def serialize(person):
    return f"Name: {person.name}, Age: {person.age}"


with open("person.txt", "w") as file:
    file.write(serialize(p1))



with open("person.txt", "r") as file:
    data = file.readline()


def deserialize(text):
    parts = text.split(", ")

    name = parts[0].replace("Name: ", "")
    age = int(parts[1].replace("Age: ", ""))

    return Person(name, age)

person2 = deserialize(data)

print(person2)

# home work 2

import json

def add_persons(count):
    with open("persons.json", "r") as file:
        persons = json.load(file)

    last_id = persons[-1]["id"]

    for i in range(count):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))

        person = {
            "id": last_id + 1,
            "name": name,
            "age": age
        }

        persons.append(person)
        last_id += 1

    with open("persons.json", "w") as file:
        json.dump(persons, file, indent=4)


add_persons(2)
