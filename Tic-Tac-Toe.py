def print_grid():
    global top, mid, bot
    horizontal_border = "---------"
    print(horizontal_border)
    print("| {} {} {} |".format(top[0],top[1], top[2]))  # printing symbols separately so it's possible to have a blankspace between each of three sybmols
    print("| {} {} {} |".format(mid[0],mid[1], mid[2]))
    print("| {} {} {} |".format(bot[0],bot[1], bot[2]))
    print(horizontal_border)

underscore = "_"

# creating check-variables, describing potential scenarios
toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win, ldialonal, rdialonal = None, None, None, None, None, None, None, None
def possible_combinations():
    # accessing global variables to make sure operations within function will change the global value
    global toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win, ldialonal, rdialonal
    # possible combinations list :
    # cheching row combinations
    if top[0] == top[1] == top[2] != underscore:  # checking if all symbols in row are the same and allow to win
        toprow_win = True
    else:
        toprow_win = False
    if mid[0] == mid[1] == mid[2] != underscore:  # checking if all symbols in row are the same and allow to win
        midrow_win = True
    else:
        midrow_win = False
    if bot[0] == bot[1] == bot[2] != underscore:  # checking if all symbols in row are the same and allow to win
        botrow_win = True
    else:
        botrow_win = False

    # checking column combinations
    if top[0] == mid[0] == bot[0] != underscore:  # checking if all symbols in column are the same and allow to win
        leftcol_win = True
    else:
        leftcol_win = False
    if top[1] == mid[1] == bot[1] != underscore:  # checking if all symbols in column are the same and allow to win
        midcol_win = True
    else:
        midcol_win = False
    if top[2] == mid[2] == bot[2] != underscore:  # checking if all symbols in column are the same and allow to win
        rightcol_win = True
    else:
        rightcol_win = False

    # Checking diagonals:
    if top[0] == mid[1] == bot[2] != underscore:  # checking if all symbols in diagonal are the same and allow to win
        ldialonal = True
    else:
        ldialonal = False
    if top[2] == mid[1] == bot[0] != underscore:  # checking if all symbols in diagonal are the same and allow to win
        rdialonal = True
    else:
        rdialonal = False


player_x = "X"
player_o = "O"
game_status = "OK"
current_player = player_x


def next_player():
    global current_player
    if current_player == player_x:
        current_player = player_o
    else:
        current_player = player_x



def user_move(step):
    #column, row = input("Enter the coordinates:").split()  #task desction was not correct
    row, column = input("Enter the coordinates:").split()

    global start, current_field
    try:
        column = int(column)
        row = int(row)
        column -= 1
        row -= 1
        if current_field[row][column] == "X":
            pass
        if current_field[row][column] == "O":
            pass
    except ValueError:
        print("You should enter numbers!")
        user_move(step)
    except IndexError:
        print("Coordinates should be from 1 to 3!")
        user_move(step)
    else:
        if current_field[row][column] == "X" or current_field[row][column] == "O":
            print("This cell is occupied! Choose another one!")
            user_move(step)
        else:
            #print(column, row)
            current_field[row][column] = step  #bug was here, equality instead of assigning
            print_grid()



def game_rules_validation():  # move rules here
    global current_field, top, mid, bot, toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win
    # checking if game is possible
    #x = top.count("X") + mid.count("X") + bot.count("X")
    #o = top.count("O") + top.count("O") + top.count("O")
    empty_cells = (top.count("_") + mid.count("_") + bot.count("_"))

    if status.count(True) > 1:  # Two winners or win "reasons" at the same time is not possible
        print("Impossible")
        exit()

    #looking for a winner on a row level
    if toprow_win:
        if top[0] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()
    elif midrow_win:
        if mid[0] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()
    elif botrow_win:
        if bot[0] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()

    #looking for a winner on a column level
    elif leftcol_win:
        if top[0] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()
    elif midcol_win:
        if top[1] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()
    elif rightcol_win:
        if top[2] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()

    #looking for a winner on a diagonal level
    elif ldialonal or rdialonal:
        if mid[1] == "O":
            print("O wins")
            exit()
        else:
            print("X wins")
            exit()
    else:
        print("Num of empty cells", empty_cells)
        if empty_cells < 1:  # at least 1 move left  # issue is here, DRAW function is not working
            print("Draw")
            exit()
        else:
            pass

#  first launch :
start = "_" * 9

start = list(start)
current_field = [start[0:3], start[3:6], start[6:9]]
top = current_field[0]
mid = current_field[1]
bot = current_field[2]
print_grid()  # print 1st grid
possible_combinations()  # Input is already taken, so we can execute the possible_combinations function and check T/F win status for each occasion
status = [toprow_win, midrow_win, botrow_win, leftcol_win, midcol_win, rightcol_win, ldialonal, rdialonal]


#while game_status != any(["Draw", "Game_over", "Impossible"]):
while True:
    possible_combinations()  # testing if adding this function here will prevent game continuation once won
    game_rules_validation()
    if current_player == player_x:
        user_move(player_x)
        next_player()
    else:
        user_move(player_o)
        next_player()
