# home work 1

numbers = [10, 20, 30, 40, 50]

total = 0
count = 0

for num in numbers:
    total += num
    count += 1

average = total / count

print( total)
print( average)

# home work 2

items = ['a', 'b', 2, 4, 2, 'c', 'j', 1, 'b', 'd', 'c', 4, 1]

unique_items = []

for item in items:
    if item not in unique_items:
        unique_items.append(item)

print(unique_items)

# home work 3

import random

numbers = []
even_numbers = []

for i in range(20):
    num = random.randint(-50, 50)
    numbers.append(num)

    if num % 2 == 0:
        even_numbers.append(num)

print(numbers)
print(even_numbers)


# home work 4

persons = [
    ('Kelly', 'Simpson', 26),
    ('Erika', 'Stephens', 24),
    ('Cheryl', 'Dunn', 30),
    ('Amy', 'Larsen', 49),
    ('Christine', 'Gordon', 23),
    ('Monica', 'Huff', 38),
    ('David', 'Nixon', 36),
    ('Cindy', 'Escobar', 41),
    ('Cindy', 'White', 33),
    ('Joel', 'Hall', 43),
    ('Steven', 'Winters', 28),
    ('Alex', 'Cole', 68),
    ('Alex', 'Smith', 32),
    ('Alex', 'White', 42),
    ('Brittany', 'Thompson', 18),
    ('Ernest', 'Young', 43),
    ('Traci', 'Wells', 38),
    ('Andrew', 'Flores', 61),
    ('Christopher', 'Lewis', 29),
    ('Kevin', 'Willis', 57),
    ('Kayla', 'Lucas', 28),
    ('Michelle', 'Rush', 43),
    ('Thomas', 'Mason', 37)
]

while True:
    name = input("Enter name: ")

    if name == "stop":
        break

    found_name = False

    for person in persons:
        if person[0] == name:
            found_name = True
            break

    if not found_name:
        print("Name not found")
        continue

    surname = input("Enter surname: ")

    if surname == "stop":
        break

    found_person = False

    for person in persons:
        if person[0] == name and person[1] == surname:
            print("Age:", person[2])
            found_person = True
            break

    if not found_person:
        print("Surname not found")