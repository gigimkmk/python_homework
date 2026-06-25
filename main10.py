# home work 1


# def numbers (count = 5 ):
#     total = 0

#     for i in range(count):
       
#         number = int(input("Enter number: "))
    
#         total += number
    
#     return total

# print (numbers ())




# home work 2


# def numbers (*args):

#     luwi = []
#     kenti = []

#     for number in args:

#         if number % 2 == 0:
#             luwi.append(number)
#         else :
#            kenti.append(number)

#     return kenti,luwi
    
# kenti, luwi = numbers(1, 2, 3, 4, 5, 6)

# print( kenti)
# print( luwi)

# # home work 3

# def count_words(sentence):
#     sentence = sentence.lower()
#     sentence = sentence.replace(".", "")

#     words = sentence.split()

#     result = {}

#     for word in words:
#         if word in result:
#             result[word] += 1
#         else:
#             result[word] = 1

#     return result


# print(count_words("This is a test. This test is fun."))


# home work 4
# from functools import reduce

# products = [
#     {"name": "Laptop", "price": 1200},
#     {"name": "Mouse", "price": 15},
#     {"name": "Keyboard", "price": 25},
#     {"name": "Monitor", "price": 150},
#     {"name": "Power", "price": 100},
#     {"name": "Pad", "price": 10},
# ]

# def less_than_100(product):
#     return product["price"] < 100

# cheap_products = list(filter(less_than_100, products))
# print(cheap_products)


# def product_info(product):
#     return product["name"], product["price"]

# info = list(map(product_info, products))
# print(info)


# def get_price(product):
#     return product["price"]

# sorted_products = sorted(products, key=get_price)
# print(sorted_products)


# def add_prices(total, product):
#     return total + product["price"]

# total_price = reduce(add_prices, products, 0)
# print(total_price)

# home work 5



def sum_recursive(n):
    if n == 1:
        return 1
    return n + sum_recursive(n - 1)

print(sum_recursive(5))