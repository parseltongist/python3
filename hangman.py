# Write your code here
import random
random.seed()
tries_remain = 8
word_list = ['python', 'java', 'kotlin', 'javascript']
guessed_letters = set()
inputed_letters = set()
low_eng = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

def menu():
    action = input('Type "play" to play the game, "exit" to quit:')
    if action == "exit":
        exit()
    elif action == "play":
        continue
    else:
        print("Incorrect option given")


word = list(random.choice(word_list))

word_masked = list('-' * len(word))
print("H A N G M A N\n")
menu()


while tries_remain > 0: #  word_masked != word:
    print(''.join(word_masked))
    letter = input('Input a letter:')
    if len(letter) > 1:
        print("You should input a single letter")
        print()
    elif letter not in low_eng:
        print("Please enter a lowercase English letter")
        print()
    elif letter in inputed_letters:
            print("You've already guessed this letter")
            print()
    else:
        inputed_letters.add(letter)
        if letter in word:
            guessed_letters.add(letter)
            for i in range(len(word)):
                if word[i] == letter:
                    word_masked[i] = letter
            if word_masked == word:
                print("You guessed the word!")
                print("You survived!")
                break
            print()
        else:
            tries_remain -= 1
            if tries_remain !=0:
                print("That letter doesn't appear in the word")
                print()
            else:
                print("That letter doesn't appear in the word")
else:
    print('You lost!')
    print()
    menu()
