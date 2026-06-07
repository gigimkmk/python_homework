# # home work 1 

text = input("Enter some text: ")
word1 = input("Enter the first word: ")
word2 = input("Enter the second word: ")

new_text = text.replace(word1, word2)

print(new_text)

# home work 2 

text = input("Enter some text: ")

words = text.split()

longest = ""

for word in words:
    if len(word) > len(longest):
      longest = word

print(longest)


# home work 3 

word1 = input("Enter the first word: ")
word2 = input("Enter the second word: ")

word1 = word1.lower()
word2 = word2.lower()

if sorted(word1) == sorted(word2):
    print("These words are anagrams.")