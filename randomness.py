final_string = ''
triadas = ["000", "001", "010", "011", "100", "101", "110", "111"]
pattern_dict = dict.fromkeys(triadas, [])


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
    print("\nFinal data string:\n{}\n".format(final_string))





for key in triadas:
    x, y = key + "0", key + "1"
    pattern_dict[key] = [final_string.count(x),final_string.count(y)]


#print("test is",test)

for key in pattern_dict:
    print(f"{key}: {pattern_dict[key][0]},{pattern_dict[key][1]}")
