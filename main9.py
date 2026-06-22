
# home work 1 

def text_info(text):
    count = 0

    for char in text:
        if char.isupper():
            count += 1

    return count, text.upper()


user_text = input("Enter text: ")

uppercase_count, upper_text = text_info(user_text)

print("Uppercase letters:", uppercase_count)
print("Text in uppercase:", upper_text)



# home work 2


def camel_to_snake(text):
    result = ""

    for char in text:
        if char.isupper():
            result += "_" + char.lower()
        else:
            result += char

    return result


print(camel_to_snake("firstName"))
print(camel_to_snake("name"))
print(camel_to_snake("preferredFirstName"))
print(camel_to_snake("lastName"))