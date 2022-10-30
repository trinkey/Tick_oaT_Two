from turtle import Turtle, Screen

turn = 1
board = [[0] * 3, [0] * 3, [0] * 3]

class Board:
    def __init__(self):
        self.screen = Screen()

        self.screen.setup(600, 600)
        self.screen.bgpic("tickoattwo/blueTurnBackground.gif")
        self.screen.tracer(0)
    
    def changeBG(self, background):
        '''Input a number, 1-4 to change the background
        1: blue turn
        2: red turn
        3: blue win
        4: red win'''
        bgs = ["", "blueTurn", "redTurn", "blueWin", "redWin"]
        self.screen.bgpic(f"tickoattwo/{bgs[background]}Background.gif")

screen = Board()

# Add shapes for turtle
screen.screen.addshape(f"tickoattwo/blueTile.gif")
screen.screen.addshape(f"tickoattwo/bothTile.gif")
screen.screen.addshape(f"tickoattwo/redTile.gif")
screen.screen.addshape(f"tickoattwo/blankTile.gif")

class TickoaTTwoIcon:
    def __init__(self, x, y):
        '''The x and y values should be 0-2
        They also correspond with the position in the list
        For example, (0, 0) would be in the neg neg quadrant, and (2, 2) would be in the pos pos quadrent'''
        coordinates = [-150, 0, 150]
        self.coords = [x, y]
        self.turtle = Turtle()
        self.turtle.pu()
        self.turtle.shape("tickoattwo/blankTile.gif")
        self.turtle.goto(coordinates[x], coordinates[y])
    
    def changeIcon(self, icon):
        '''Changes icon of current tile
        0: blank
        1: blue
        2: red
        3: both'''
        global board

        if icon == 1 or icon == 2:
            if board[self.coords[0]][self.coords[1]] != 0:
                icon = 3

        board[self.coords[0]][self.coords[1]] = icon

        if not icon:
            self.turtle.shape("tickoattwo/blankTile.gif")
        elif icon == 1:
            self.turtle.shape("tickoattwo/blueTile.gif")
        elif icon == 2:
            self.turtle.shape("tickoattwo/redTile.gif")
        elif icon == 3:
            self.turtle.shape("tickoattwo/bothTile.gif")

# Appends the tiles in an order that makes it left to right, bottom to top
tiles = []
for i in range(3):
    temp = []
    for o in range(3):
        temp.append(TickoaTTwoIcon(o, i))
    tiles.append(temp)
del(temp)

checks = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

def checkForWin():
    global checks, board
    for i in checks:
        if board[i[0] % 3][i[0] // 3] == board[i[1] % 3][i[1] // 3] == board[i[2] % 3][i[2] // 3] == 3:
            return 1
    return 0

def incrementTurn(turn):
    if turn == 1:
        return 2
    return 1

previous = [-1, -1]

def clickEvent(x, y):
    global turn, board, previous
    newprevious = [-1, -1]
    if x > -265 and x < -72:
        xcor = 0
        newprevious[0] = 0
    elif x < 72:
        xcor = 1
        newprevious[0] = 1
    elif x < 265:
        xcor = 2
        newprevious[0] = 2
    else:
        xcor = -1

    if y > -265 and y < -72:
        ycor = 0
        newprevious[1] = 0
    elif y < 72:
        ycor = 1
        newprevious[1] = 1
    elif y < 265:
        ycor = 2
        newprevious[1] = 2
    else:
        ycor = -1

    if xcor + 1 and ycor + 1 and (board[xcor][ycor] == 0 or board[xcor][ycor] == 1 or board[xcor][ycor] == 2) and not (xcor == previous[0] and ycor == previous[1]) and board[xcor][ycor] != turn:
        # Update tile elements
        tiles[ycor][xcor].changeIcon(turn)

        # Increment the turn and update the screen
        if checkForWin():
            screen.changeBG(turn + 2)
            screen.screen.onclick(die)
            for i in tiles:
                for o in i:
                    o.turtle.hideturtle()
        else:
            turn = incrementTurn(turn)
            screen.changeBG(turn)
        screen.screen.update()
        
    if not newprevious.count(-1):
        previous = [newprevious[0], newprevious[1]]

def die(x = 0, y = 0):
    screen.screen.bye()

screen.screen.onclick(clickEvent)
screen.screen.update()
screen.screen.mainloop()
# -265 to 265 vertically and horizontally
# -72 to 72 for the smaller ones
# That could cause some inconsistencies with the curvieness of the board