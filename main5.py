# home work 1

try:
    age = int(input("Enter your age: "))

    if  age < 0:
        raise  ValueError("Age canot be negative!")

except:
    print ("Please enter numbers only!")

else:
    if age < 18:
        print("Minor")
    else:
        print("Adult")





# home woek 2


try : 
    num1 = float(input("Enter your number :"))
    num2 = float(input("Enter your number :" ))
    number = (num1/num2)


except ValueError:
    print("Please enter only numbers!")

except ZeroDivisionError:
    print("Cannot divide by zero!")

except Exception as e:
    print("Unknown error!")
    print(e)
else :
    print("Result", number)
finally:
    print("Program finished")


    # test file rom gamovagzavne shemeshala py ar mivuwere wertilis  shemdeg da shesabamisad ubralod texturi avtvirte exla gadavakete da tavidan avtvirte da aqac cahvsvam  :)