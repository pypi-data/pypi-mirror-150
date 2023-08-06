

#words = ['apple', 'banana', 'doodke', 'test']

#print(' '.join(words))
word = []

def checkIfDone():

    f = "".join(word)

    if f == "banana":
        print(word)
        print("good job!")
    else:
        print(word)
        print("no...")

i = 0 
while i == 0:
    letter = input("The letter:\n")

    if letter == "cancel":
        i = 1
        break
    if letter == "done":
        checkIfDone()

    word.append(letter)

    print('The word right now is:' + ''.join(word))
    