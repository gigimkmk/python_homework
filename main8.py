# home work 1



# squares = {number: number ** 2 for number in range(1, 11)}

# print(squares)




# # home work 2


# products = [
#     {"cola": {
#         "price": 1.5,
#         "quantity": 10
#     }},
#     {"fanta": {
#         "price": 2.5,
#         "quantity": 5
#     }},
#     {"snickers": {
#         "price": 3.5,
#         "quantity": 12
#     }},
#     {"water": {
#         "price": 4.5,
#         "quantity": 8
#     }},
#     {"beer": {
#         "price": 6.5,
#         "quantity": 5
#     }}
# ]

# total = 0

# for product in products:
#     for name, info in product.items():
#         print(name)
#         total += info["price"] * info["quantity"]

# print("Total value:", total)




# home work 3

fruits = {}

while True:
    fruit = input("Enter your favorite fruit: ")

    if fruit == "stop":
        break

    if fruit in fruits:
        fruits[fruit] += 1
    else:
        fruits[fruit] = 1

print(fruits)