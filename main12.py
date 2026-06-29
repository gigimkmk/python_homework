# home work 1

# def commission(func):
#     def wrapper(balance, amount):
#         amount = amount + 1  

#         if balance < amount:
#             return "arasakmarisi tanxa angarishze!"

#         return func(balance, amount)

#     return wrapper


# @commission
# def transaction(balance, amount):
#     return balance - amount


# print(transaction(100, 50))  
# print(transaction(50, 50))

# home work 2


def count_calls(func):
    count = 0

    def wrapper():
        nonlocal count
        count += 1
        print(f"Function called {count} times")
        return func()

    return wrapper


@count_calls
def hello():
    print("Hello")


hello()
hello()
hello()