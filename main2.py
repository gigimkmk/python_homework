# home work 1

a = int(input("Enter first leg: "))
b = int(input("Enter second leg: "))

c = (a**2 + b**2) ** 0.5
s = a * b / 2
print("Hypotenuse =", c)
print("Area =", s)

# home work 2

a = int(input("Enter seconds: "))

hours = a // 3600
minutes = (a % 3600) // 60
seconds = a % 60

print("Hours:", hours)
print("Minutes:", minutes)
print("Seconds:", seconds)