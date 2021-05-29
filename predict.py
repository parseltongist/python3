# creating check-variables, describing potential scenarios
toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win, ldialonal, rdialonal = None, None, None, None, None, None, None, None
def possible_combinations():
    # accessing global variables to make sure operations within function will change the global value
    global toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win, ldialonal, rdialonal
    # possible combinations list :
    # cheching row combinations
    if top[0] == top[1] == top[2]:  # checking if all symbols in row are the same and allow to win
        toprow_win = True
    else:
        toprow_win = False
    if mid[0] == mid[1] == mid[2]:  # checking if all symbols in row are the same and allow to win
        midrow_win = True
    else:
        midrow_win = False
    if bot[0] == bot[1] == bot[2]:  # checking if all symbols in row are the same and allow to win
        botrow_win = True
    else:
        botrow_win = False

    # checking column combinations
    if top[0] == mid[0] == bot[0]:  # checking if all symbols in column are the same and allow to win
        leftcol_win = True
    else:
        leftcol_win = False
    if top[1] == mid[1] == bot[1]:  # checking if all symbols in column are the same and allow to win
        midcol_win = True
    else:
        midcol_win = False
    if top[2] == mid[2] == bot[2]:  # checking if all symbols in column are the same and allow to win
        rightcol_win = True
    else:
        rightcol_win = False

    # Checking diagonals:
    if top[0] == mid[1] == bot[2]:  # checking if all symbols in diagonal are the same and allow to win
        ldialonal = True
    else:
        ldialonal = False
    if top[2] == mid[1] == bot[0]:  # checking if all symbols in diagonal are the same and allow to win
        rdialonal = True
    else:
        rdialonal = False


top_border = "---------"
start = input("Enter cells:\n")

if len(start) == 9:
    top= start[0:3]
    mid = start[3:6]
    bot = start[6:9]
    print(top_border)
    print("| {} {} {} |".format(top[0],top[1], top[2]))  # printing symbols separately so it's possible to have a blankspace between each of three sybmols
    print("| {} {} {} |".format(mid[0],mid[1], mid[2]))
    print("| {} {} {} |".format(bot[0],bot[1], bot[2]))
    print(top_border)


    x = start.count("X")
    o = start.count("O")
    possible_combinations()  # Input is already taken, so we can execute the possible_combinations function and check T/F win status for each occasion
    status = [toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win, ldialonal, rdialonal]

    # checking if game is possible
    if abs(x-o) > 1:  # the difference between the number of X and 0 sings can't be more than 1 players make a move one by one
        print("Impossible")  # 19
        exit()


    if status.count(True) > 1:  # Two winners or win "reasons" at the same time is not possible
        print("Impossible")
        exit()

    #looking for a winner on a row level
    if toprow_win:
            if top[0] == "O":
                print("O wins")
            else:
                print("X wins")
    elif midrow_win:
        if mid[0] == "O":
            print("O wins")
        else:
            print("X wins")
    elif botrow_win:
        if bot[0] == "O":
            print("O wins")
        else:
            print("X wins")

    #looking for a winner on a column level
    elif leftcol_win:
        if top[0] == "O":
            print("O wins")
        else:
            print("X wins")
    elif midcol_win:
        if top[1] == "O":
            print("O wins")
        else:
            print("X wins")
    elif rightcol_win:
        if top[2] == "O":
            print("O wins")
        else:
            print("X wins")

    #looking for a winner on a diagonal level
    elif ldialonal or rdialonal:
        if mid[1] == "O":
            print("O wins")
        else:
            print("X wins")
    else:
        if x + o < 9:  # at least 1 move left
            print("Game not finished")
        else:  # "no moves left"
            print("Draw")

else:
    print("INCORRECT INPUT")
