import json
import time

FILE_NAME = "C:/Users/Gigi/Desktop/project/middle exam/dictionary.json"


def load_dictionary():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("dictionary.json ფაილი ვერ მოიძებნა.")
        return {}

    except json.JSONDecodeError:
        print("JSON ფაილის ფორმატი არასწორია.")
        return {}


def save_dictionary(dictionary):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)



dictionary = load_dictionary()


while True:

    print("\n====== თარჯიმანი ======")
    print("1. ინგლისური -> ქართული")
    print("2. ქართული -> ინგლისური")
    print("3. გასვლა")

    choice = input("აირჩიეთ: ").strip()


    if choice == "3":
        print("პროგრამა იხურება...")
        time.sleep(1)
        break


    if choice not in ["1", "2"]:
        print("არასწორი არჩევანი!")
        continue


    word = input("შეიყვანეთ სიტყვა: ").strip()


    if choice == "1":

        if not word.isascii():
            print("გთხოვთ შეიყვანოთ ინგლისური სიტყვა.")
            continue


        word = word.lower()

        print("ვეძებ თარგმანს....")
        time.sleep(1)


        if word in dictionary:

            print("თარგმანი:", dictionary[word])


        else:

            print("სიტყვა ვერ მოიძებნა.")

            answer = input("დავამატოთ? (yes/no): ").lower()


            if answer == "yes":

                translation = input(
                    "შეიყვანეთ ქართული თარგმანი: "
                )


                dictionary[word] = translation

                save_dictionary(dictionary)

                print("სიტყვა დაემატა.")



    elif choice == "2":

        if word.isascii():
            print("გთხოვთ შეიყვანოთ ქართული სიტყვა.")
            continue


        print("ვეძებ თარგმანს...")
        time.sleep(1)


        found = False


        for english, georgian in dictionary.items():

            if georgian == word:

                print("თარგმანი:", english)

                found = True
                break



        if not found:

            print("სიტყვა ვერ მოიძებნა.")

            answer = input("დავამატოთ? (yes/no): ").lower()


            if answer == "yes":

                english = input(
                    "შეიყვანეთ ინგლისური სიტყვა: "
                )


                dictionary[english.lower()] = word

                save_dictionary(dictionary)

                print("სიტყვა დაემატა.")