import random

print("Welcome to Connect Four")

# Initialize the game board
gameBoard = [["" for _ in range(7)] for _ in range(6)]

rows = 6
cols = 7

def printboard():
    """
    Prints the current state of the game board to the console.
    """
    print("\n    1    2    3    4    5    6    7")
    for x in range(rows):
        n=abs(x-6)
        print("  +----+----+----+----+----+----+----+")
        print(x+1, "|", end="")
        for y in range(cols):
            if gameBoard[x][y] == "o":
                print(" o", end="  |")
            elif gameBoard[x][y] == "*":
                print(" *", end="  |")
            elif gameBoard[x][y] == "x":
                print(" x", end="  |")
            else:
                print("  ", end="  |")
        print(" ", x+1)
    print("  +----+----+----+----+----+----+----+")
    print("    1    2    3    4    5    6    7")

def modify_array(pickedspace, turn):
    """
    Modifies the game board at the specified coordinates.
    
    Parameters:
    pickedspace (list): A list containing the row and column to modify.
    turn (str): The marker ("o", "*", "x") to place on the game board.
    """
    gameBoard[pickedspace[0]][pickedspace[1]] = turn

def clear_grid():
    """
    Resets the game board to its initial empty state.
    """
    global gameBoard
    gameBoard = [["" for _ in range(7)] for _ in range(6)]

def win_check(disc):
    """
    Checks if the given disc has won the game.

    Parameters:
    disc (str): The disc to check for a win ("o", "*", "x").

    Returns:
    bool: True if the disc has won, False otherwise.
    """
    # Check horizontal
    for y in range(rows):
        for x in range(cols - 3):
            if gameBoard[y][x] == disc and gameBoard[y][x + 1] == disc and gameBoard[y][x + 2] == disc and gameBoard[y][x + 3] == disc:
                return True

    # Check vertical
    for x in range(cols):
        for y in range(rows - 3):
            if gameBoard[y][x] == disc and gameBoard[y + 1][x] == disc and gameBoard[y + 2][x] == disc and gameBoard[y + 3][x] == disc:
                return True

    # Check diagonal (upper right to bottom left)
    for x in range(rows - 3):
        for y in range(3, cols):
            if gameBoard[x][y] == disc and gameBoard[x + 1][y - 1] == disc and gameBoard[x + 2][y - 2] == disc and gameBoard[x + 3][y - 3] == disc:
                return True

    # Check diagonal (top left to bottom right)
    for x in range(rows - 3):
        for y in range(cols - 3):
            if gameBoard[x][y] == disc and gameBoard[x + 1][y + 1] == disc and gameBoard[x + 2][y + 2] == disc and gameBoard[x + 3][y + 3] == disc:
                return True

    return False

def coordinate_adder(inputstr):
    """
    Converts user input into board coordinates.

    Parameters:
    inputstr (list): A list containing the row and column input as strings.

    Returns:
    list: A list containing the conveted row and column as integers.
    """
    coordinate = [None] * 2
    coordinate[0] = int(inputstr[0]) - 1
    coordinate[1] = int(inputstr[1]) - 1
    return coordinate

def space_check(coords):
    """
    Checks if the specified space on the board is empty.

    Parameters:
    coords (list): A list containing the row and column to check.

    Returns:
    bool: True if the space is empty, False otherwise.
    """
    return gameBoard[coords[0]][coords[1]] == ""

def gravity_check(inputs):
    """
    Checks if the specified space follows gravity rules (i.e., if the space below it is occupied or it's on the bottom row).

    Parameters:
    inputs (list): A list containing the row and column to check.

    Returns:
    bool: True if the space follows gravity rules, False otherwise.
    """
    space_under = [None] * 2
    space_under[0] = inputs[0] + 1
    space_under[1] = inputs[1]
    if space_under[0] == rows or gameBoard[space_under[0]][space_under[1]] != "":
        return True
    return False

def recommend_column():
    """
    Recommends a random column for the next move.

    Returns:
    int: The recommended column index.
    """
    while True:
        col = random.randint(0, cols - 1)
        if gameBoard[0][col] == "":
            return col

def improved_recommendation(disc):
    """
    Recommends a column for the next move, prioritizing winning moves.

    Parameters:
    disc (str): The disc to check for winning moves ("o", "*", "x").

    Returns:
    int: The recommended column index.
    """
    for col in range(cols):
        if gameBoard[0][col] == "":
            for row in range(rows - 1, -1, -1):
                if gameBoard[row][col] == "":
                    gameBoard[row][col] = disc
                    if win_check(disc):
                        gameBoard[row][col] = ""
                        return col
                    gameBoard[row][col] = ""
                    break
    return recommend_column()

def oneplayer():
    """
    Handles the gameplay for a single-player game against the computer.
    """
    leaveLoop = False
    turn_count = 0
    while not leaveLoop:
        # User's turn
        if turn_count % 2 == 0:
            printboard()
            print("\nRecommended column: " + str(improved_recommendation("o") + 1))
            while True:
                pickedspace = input("(o) Choose a space: ").split()
                if len(pickedspace) != 2 or not pickedspace[0].isdigit() or not pickedspace[1].isdigit():
                    print("Invalid input. Please enter row and column as numbers.")
                    continue
                coordinate = coordinate_adder(pickedspace)
                try:
                    if space_check(coordinate) and gravity_check(coordinate):
                        modify_array(coordinate, "o")
                        break
                    else:
                        print("Not a valid coordinate")
                except Exception as e:
                    print(f"Error occurred: {e}. Please try again.")
            if win_check("o"):
                printboard()
                print("\nGame over, Player1 wins! Thank you for playing :)")
                break
            turn_count += 1
        else:
            # Computer's turn
            while True:
                compchoice = improved_recommendation("*")
                coordinate = [0, compchoice]
                for row in range(rows - 1, -1, -1):
                    if gameBoard[row][compchoice] == "":
                        coordinate[0] = row
                        break
                if space_check(coordinate) and gravity_check(coordinate):
                    modify_array(coordinate, "*")
                    break
            if win_check("*"):
                printboard()
                print("\nGame over, Computer wins! Thank you for playing :)")
                break
            turn_count += 1

def twoplayer():
    """
    Handles the gameplay for a two-player game.
    """
    leaveLoop = False
    turn_count = 0
    while not leaveLoop:
        # Player1's turn
        if turn_count % 2 == 0:
            printboard()
            print("Player1's (o) Turn...") 
            print("\nRecommended column: " + str(improved_recommendation("o") + 1))
            while True:
                pickedspace = input("Choose a space: ").split()
                if len(pickedspace) != 2 or not pickedspace[0].isdigit() or not pickedspace[1].isdigit():
                    print("Invalid input. Please enter row and column as numbers.")
                    continue
                coordinate = coordinate_adder(pickedspace)
                try:
                    if space_check(coordinate) and gravity_check(coordinate):
                        modify_array(coordinate, "o")
                        break
                    else:
                        print("Not a valid coordinate")
                except Exception as e:
                    print(f"Error occurred: {e}. Please try again.")
            if win_check("o"):
                printboard()
                print("\nGame over, Player1(o) wins! Thank you for playing :)")
                break
            turn_count += 1
        else:
        # Player2's turn
            printboard()
            print("Player2's (x) Turn...") 
            print("\nRecommended column: " + str(improved_recommendation("x") + 1))
            while True:
                pickedspace = input("Choose a space: ").split()
                if len(pickedspace) != 2 or not pickedspace[0].isdigit() or not pickedspace[1].isdigit():
                    print("Invalid input. Please enter row and column as numbers.")
                    continue
                coordinate = coordinate_adder(pickedspace)
                try:
                    if space_check(coordinate) and gravity_check(coordinate):
                        modify_array(coordinate, "x")
                        break
                    else:
                        print("Not a valid coordinate")
                except Exception as e:
                    print(f"Error occurred: {e}. Please try again.")
            if win_check("x"):
                printboard()
                print("\nGame over, Player2(x) wins! Thank you for playing :)")
                break
            turn_count += 1

def game_selection():
    '''
    Allows the user to select between one-player and two-player game modes.
    '''
    game_select = input("Which game do you want to play? \n1) Player1 vs Computer \n2) Player1 vs Player2 \nEnter the number of the game you selected: ")
    if game_select == "1":
        print("-----------------------")
        print("Enter Coordinates for playing the game. First type row and then column. (For example - 3 5 -> there you selected row as 3 and column as 5)")
        print("\nYour disc: o    Computer's disc: x")
        oneplayer()
        game_restart()
    elif game_select == "2":
        print("-----------------------")
        print("Enter Coordinates for playing the game. First type row and then column. (For example - 3 5 -> there you selected row as 3 and column as 5)")
        print("\nPlayer1's disc: o    Player2's disc: x")
        twoplayer()
        game_restart()
    else:
        print("Invalid input. Please try again....")
        game_selection()


def game_restart():
    '''
    Restarts the game or exits based on the user's input.
    '''
    clear_grid()
    ans=input("Do you want to play again? [y/n]: ")
    if ans == "y":
        game_selection()
    elif ans == "n":
        print("Exiting program...")
    else:
        print("Invalid input. Please try again....")
        game_restart()
        
def test_win_check():
    '''
    Tests the win_check function.
    
    This function tests the win_check() to ensure that it correctly identifies 
    when a player has won in horizontal, vertical, and diagonal directions.
    '''
    global gameBoard

    # test horizontal 
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[0][0] = gameBoard[0][1] = gameBoard[0][2] = gameBoard[0][3] = "o"
    assert win_check("o") == True

    # test vertical win
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[0][0] = gameBoard[1][0] = gameBoard[2][0] = gameBoard[3][0] = "x"
    assert win_check("x") == True

    # test for diagonal_2 (top-left to bottom-right) win
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[0][0] = gameBoard[1][1] = gameBoard[2][2] = gameBoard[3][3] = "o"
    assert win_check("o") == True

    # test diagonal2 (top-right to bottom-left) win
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[0][3] = gameBoard[1][2] = gameBoard[2][1] = gameBoard[3][0] = "x"
    assert win_check("x") == True

    # test no win
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[0][0] = "o"
    assert win_check("o") == False
    clear_grid()


def test_space_check():
    '''
    Tests the space_check function.
    
    This function ensures that space_check() correctly identifies whether a 
    space is empty on the game board.
    '''
    global gameBoard
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[0][0] = "o"
    assert space_check([0, 0]) == False  
    assert space_check([1, 1]) == True   
    clear_grid()


def test_gravity_check():
    '''
    Tests the gravity_check function.
    
    This function ensures that gravity_check() correctly identifies whether a 
    disc can be placed in a certain position based on gravity rules.
    '''
    global gameBoard
    gameBoard = [["" for _ in range(7)] for _ in range(6)]
    gameBoard[4][0] = "o"
    assert gravity_check([5, 0]) == True  
    clear_grid()



if __name__ == "__main__":
    test_win_check()
    test_space_check()
    test_gravity_check()
    game_selection()

