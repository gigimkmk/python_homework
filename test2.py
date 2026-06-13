import random

number = random.randint (1, 100)

lives = 5

while lives > 0 :
    user = int(input("Enter your number :"))
    
    if user == number :
        print("you won")
        break
    if user > number:
        print("your number is lower")
    else :
        print("your number is higher")

        lives -= 1
    print("Lives:", lives)

if lives == 0:
    print("You lost!")

        