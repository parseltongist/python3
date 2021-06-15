final_string = ''
triadas = ["000", "001", "010", "011", "100", "101", "110", "111"]
pattern_dict = dict.fromkeys(triadas, [])
balance = 1000


def welcome_message():
    print("""
Please give AI some data to learn...
The current data length is 0, 100 symbols left""")


def print_rules():
    print("""
You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!""")


def data_to_learn():
    global final_string, triadas, pattern_dict
    while len(final_string) < 100:
        string = input("Print a random string containing 0 or 1:\n\n")
        for symbol in string:
            if symbol == "0" or symbol == "1":
                final_string += symbol
        if len(final_string) < 100:
            print(f"Current data length is {len(final_string)}, {100 - len(final_string)} symbols left")
        else:
            pass
    else:
        print("\nFinal data string:\n{}\n\n".format(final_string))

    for key in triadas:
        x, y = key + "0", key + "1"
        pattern_dict[key] = [final_string.count(x),final_string.count(y)]


def prediction(test_string):
    global pattern_dict, balance
    prediction_string = "101"
    total_len = len(test_string)
    for number in range(total_len-3):  # decreasing by 3 as the first three random symbols are already set and we still need not to exceed the length of the line
        triad = test_string[number:number + 3]
        if pattern_dict[triad][0] >= pattern_dict[triad][1]:
            prediction_string += '0'
        else:
            prediction_string += '1'
        # or prediction_string += '0' if pattern_dict[triad][0] >= pattern_dict[triad][1] else '1'
    correctly_predicted = 0
    for x in range(3, total_len):  # issue was here, as we need to count correct matches starting from number 3 only
        if prediction_string[x] == test_string[x]:
            correctly_predicted += 1
    not_guessed_points = (total_len-3) - correctly_predicted
    balance = balance - correctly_predicted + not_guessed_points
    print(f"prediction:\n{prediction_string}\n")
    print(f"Computer guessed right {correctly_predicted} out of {total_len} symbols ({(correctly_predicted / (total_len -3) * 100):.2f} %)")  # total_len -3 here because we are not interested in all symbols but without first three.
    print(f"Your capital is now ${balance}")
    return gameplay()


def gameplay():
    players_string = input("Print a random string containing 0 or 1:\n\n")
    if players_string.lower() == "enough":
        print("Game over!")
        exit()
    elif players_string.count("0") + players_string.count("1") == len(players_string):
        prediction(players_string)
    else:
        return gameplay()  # return or just running?


welcome_message()
data_to_learn()
print_rules()
gameplay()
