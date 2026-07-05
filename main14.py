# home work 1

# count = 1

# with open("people.txt", "w") as file:
#     while True:
#         first_name = input("Enter your first name: ")

#         if first_name == "stop":
#             break

#         last_name = input("Enter your last name: ")

#         file.write(f"{count}. {first_name} {last_name}\n")

        # count += 1


# home work 2

# with open("persons.txt", "r") as file:
#     lines = file.readlines()

# with open("under_50.txt", "w") as under_50, open("over_50.txt", "w") as over_50:
#     for line in lines:
#         parts = line.strip().split(", ")

#         age = int(parts[1])

#         if age < 50:
#             under_50.write(line)
#         elif age > 50:
#             over_50.write(line)


# home work 3

# import csv

# def save_people(count):
#     with open("persons.csv", "a", newline="") as file:
#         fieldnames = ["ID", "first_name", "last_name", "age"]
#         writer = csv.DictWriter(file, fieldnames=fieldnames)

#         writer.writeheader()

#         for i in range(1, count + 1):
#             first_name = input("Enter first name: ")
#             last_name = input("Enter last name: ")

#             while True:
#                 try:
#                     age = int(input("Enter age: "))
#                     break
#                 except ValueError:
#                     print("Age must be an integer!")

#             writer.writerow({
#                 "ID": i,
#                 "first_name": first_name,
#                 "last_name": last_name,
#                 "age": age
#             })

# save_people(3)


# home work 4

import csv

with open("students.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames

    with open("failed_students.csv", "w", newline="", encoding="utf-8") as failed_file, \
         open("passed_students.csv", "w", newline="", encoding="utf-8") as passed_file:

        failed_writer = csv.DictWriter(failed_file, fieldnames=fieldnames)
        passed_writer = csv.DictWriter(passed_file, fieldnames=fieldnames)

        failed_writer.writeheader()
        passed_writer.writeheader()

        for row in reader:
            grade = int(row["Grade"])

            if grade < 50:
                failed_writer.writerow(row)
            elif grade > 50:
                passed_writer.writerow(row)