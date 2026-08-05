import json
import time

filename = "C:/Users/Gigi/Desktop/project/middle exam 2 oop/books.json"


class Book:
    def __init__(self, title, author, year, quantity=1, borrowed=0):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__quantity = quantity
        self.__borrowed = borrowed

    def get_title(self):
        return self.__title

    def borrow_book(self):
        if self.__quantity > 0:
            self.__quantity -= 1
            self.__borrowed += 1
            print("წიგნი წარმატებით გაიტანეთ.")
        else:
            print("წიგნი გატანილია და აღარ არის ხელმისაწვდომი.")

    def return_book(self):
        if self.__borrowed > 0:
            self.__borrowed -= 1
            self.__quantity += 1
            print("წიგნი წარმატებით დაბრუნდა.")
        else:
            print("ეს წიგნი გატანილი არ არის.")

    def to_dict(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "year": self.__year,
            "quantity": self.__quantity,
            "borrowed": self.__borrowed
        }

    def __str__(self):

        if self.__quantity > 0:
            status = "ხელმისაწვდომია"
        else:
            status = "გატანილია"

        return (
            f"სათაური: {self.__title} | "
            f"ავტორი: {self.__author} | "
            f"წელი: {self.__year} | "
            f"სტატუსი: {status} | "
            f"დარჩენილი რაოდენობა: {self.__quantity}"
        )


class BookManager:

    def __init__(self, filename):
        self.filename = filename
        self.books = []
        self.load_books()


    def load_books(self):

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)


            for item in data:

                book = Book(
                    item["title"],
                    item["author"],
                    item["year"],
                    item.get("quantity", 1),
                    item.get("borrowed", 0)
                )

                self.books.append(book)


        except FileNotFoundError:

            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

            self.books = []


        except json.JSONDecodeError:

            print("JSON ფაილი დაზიანებულია.")
            self.books = []



    def save_books(self):

        data = []

        for book in self.books:
            data.append(book.to_dict())


        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )



    def add_book(self, book):

        self.books.append(book)
        self.save_books()

        print("\nწიგნი წარმატებით დაემატა!")
        print(
            "დრო:",
            time.strftime("%d-%m-%Y %H:%M:%S")
        )



    def show_books(self):

        if not self.books:
            print("წიგნები არ არის.")
            return


        print("\n===== წიგნების სია =====")

        for index, book in enumerate(self.books, start=1):
            print(index, book)



    def search_book(self, title):

        for book in self.books:

            if book.get_title().lower() == title.lower():

                print("\nნაპოვნია:")
                print(book)
                return


        print("წიგნი ვერ მოიძებნა.")



    def borrow_book(self, title):

        for book in self.books:

            if book.get_title().lower() == title.lower():

                book.borrow_book()
                self.save_books()
                return


        print("წიგნი ვერ მოიძებნა.")



    def return_book(self, title):

        for book in self.books:

            if book.get_title().lower() == title.lower():

                book.return_book()
                self.save_books()
                return


        print("წიგნი ვერ მოიძებნა.")


def input_year():

    while True:

        year = input("შეიყვანეთ გამოცემის წელი: ")

        if year.isdigit():
            return int(year)

        print("შეიყვანეთ მხოლოდ რიცხვი.")



def input_quantity():

    while True:

        quantity = input("შეიყვანეთ რაოდენობა: ")

        if quantity.isdigit():
            return int(quantity)

        print("შეიყვანეთ მხოლოდ რიცხვი.")


def main():

    print("იტვირთება სისტემა...")
    time.sleep(1)


    manager = BookManager(filename)


    while True:

        print("""
========== წიგნების მართვის სისტემა ==========

1. წიგნის დამატება
2. ყველა წიგნის ნახვა
3. წიგნის ძებნა
4. წიგნის გატანა
5. წიგნის დაბრუნება
6. გამოსვლა

""")


        choice = input("აირჩიეთ მოქმედება: ")



        if choice == "1":

            title = input("სათაური: ").strip()
            author = input("ავტორი: ").strip()

            if not title or not author:
                print("ველი ცარიელი არ შეიძლება იყოს.")
                continue


            year = input_year()
            quantity = input_quantity()


            book = Book(
                title,
                author,
                year,
                quantity
            )


            manager.add_book(book)


        elif choice == "2":

            manager.show_books()



        elif choice == "3":

            title = input("საძიებო სათაური: ")

            manager.search_book(title)



        elif choice == "4":

            title = input("რომელი წიგნი გაგაქვთ?: ")

            manager.borrow_book(title)



        elif choice == "5":

            title = input("წიგნი დაბრუნებულია: ")

            manager.return_book(title)



        elif choice == "6":

            print("პროგრამა დასრულდა.")
            break



        else:

            print("არასწორი არჩევანი.")



if __name__ == "__main__":
    main()