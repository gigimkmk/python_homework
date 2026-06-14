# home work 1


number = int(input("enter your number :"))

factorial = 1

for i in range (1 , number +1) :


    factorial *= 1

print("factorial ", factorial)


# home work 2

for i in range (1, 10) :
    for j in range (1, 10):
        print(f"{i} * {j} = {i * j}")

# home work 3

amount = 50

print("Amount Due:", amount)

while amount > 0:
    bill = int(input("Insert bill: "))

    if bill == 5 or bill == 10 or bill == 20:
        amount -= bill

        if amount > 0:
            print("Amount Due:", amount)
    else:
        print("Insert a valid bill!")

change = abs(amount)

print("Change Owed:", change)