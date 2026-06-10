# # # home work 1 

weight = float(input("Enter your weight (kg): "))
height = float(input("Enter your height (m): "))

bmi = weight / (height ** 2)

print("BMI =", round(bmi, 2))

if bmi < 19:
    print("You are underweight.")
elif 19 <= bmi <= 25:
    print("You are normal weight.")
else:
    print("You are overweight.")

    # home work 2 
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
operator = input("Enter operator (+, -, *, /): ")

if operator == "+":
    print("Result =", num1 + num2)
elif operator == "-":
    print("Result =", num1 - num2)
elif operator == "*":
    print("Result =", num1 * num2)
elif operator == "/":
    if num2 != 0:
        print("Result =", num1 / num2)
    else:
        print("Error: Division by zero is not allowed.")
else:
    print("Invalid operator.")

    # home work 3 

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
num3 = float(input("Enter third number: "))

if num1 == num2 or num1 == num3 or num2 == num3:
    print("Please enter different numbers.")
else:
    if num1 > num2 and num1 > num3:
        print("Largest number is:", num1)
    elif num2 > num1 and num2 > num3:
        print("Largest number is:", num2)
    else:
        print("Largest number is:", num3)
