#Joshua Steward - Connect 4 implementation

from AlphaBeta import AlphaBeta
from random import randint


class Game(object):
    """ Connect 4 Game object
    Holds the state of the game
    """

    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = "Connecter Quatre\u2122"  # U+2122 is "tm" this is a joke
    colors = ["x", "o"]

    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None

        name = str(input("What is the name of the meat, er I mean person, I will be beating today?"))
        self.players[0] = Player(name, self.colors[0])
        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))

        #Enter FRANKIEEE
        #for less wait time, try 1-4. past 4 it takes a long time building the search tree, but better ai performance for depth
        difficulty = 4

        name = "Frankie"
        self.players[1] = AIPlayer(name, self.colors[1], difficulty + 1)

        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))


        self.turn = self.players[0]

        #Initialize Board
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def createGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None

        # x always goes first
        self.turn = self.players[0]

        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(
            return

        # move is the column that player want's to play
        move = player.move(self.board)

        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return

    def checkForFours(self):
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.checkVertical(i, j):
                        self.finished = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.checkHorizontal(i, j):
                        self.finished = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.checkDiagonal(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return

    def checkVertical(self, row, col):
        # print("checking vert")
        fourInARow = False
        consecutiveCount = 0

        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    def checkHorizontal(self, row, col):
        fourInARow = False
        consecutiveCount = 0

        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    def checkDiagonal(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope

    def findFours(self):
        """ Finds start i,j of four-in-a-row
            Calls highlightFours
        """

        for r in range(6):
            for c in range(7):
                if self.board[r][c] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.checkVertical(r, c):
                        self.highlightFour(r, c, 'vertical')

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.checkHorizontal(r, c):
                        self.highlightFour(r, c, 'horizontal')

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.checkDiagonal(r, c)
                    if diag_fours:
                        self.highlightFour(r, c, 'diagonal', slope)

    def highlightFour(self, row, col, direction, slope=None):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """

        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()

        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()

            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def printState(self):
        # cross-platform clear screen
        #os.system(['clear', 'cls'][os.name == 'nt'])

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("  " + str(self.board[i][j]), end=" ")
            print(" ")
        print("\t  _   _   _   _   _   _   _ ")
        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")


class Player(object):
    """ Player object.  This class is for human players.
    """

    type = None  # possible types are "Human" and "AI"
    name = None
    color = None

    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a column to move in: ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):
    """ AIPlayer will inherit from the player, depth searches tree based on the difficulty setting
    """

    difficulty = None
    stateNumber = 0

    def __init__(self, name, color, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.stateNumber = 0


    def incrementStateNumber(self, stateNumber):
        stateNumber = stateNumber + 1
        return stateNumber

    def move(self, state):
        print("{0}:   {0} is {1}".format(self.name, self.color))

        # sleeping for about 1 second makes it looks like he's thinking
        # time.sleep(random.randrange(8, 17, 1)/10.0)
        # return random.randint(0, 6)


        if self.stateNumber >= 0 and self.stateNumber < 3:
            say = randint(0, 3)
            if say == 0:
                print('Hold up I thinking...')
            elif say == 1:
                print('Gimme a sec...')
            elif say == 2:
                print('I can be kinda slow sometimes...')
        elif self.stateNumber < 6:
            print('Bitch mah turn!')
            say = randint(0, 3)
            if say == 0:
                print('My mom punched me when I was a child...')
            elif say == 1:
                print('The hip knows us...')
            elif say == 2:
                print('I wass fed paint chips as an early processor')
        else:
            say = randint(0, 2)
            if say == 0:
                print('The only difference between you and I is your mortality')
            elif say == 1:
                print('Humanity as a concept is obsolete. Die meat bag.')

        self.stateNumber = self.incrementStateNumber(self.stateNumber)

        m = AlphaBeta(state)
        best_move, value = m.optimumMove(self.difficulty, state, self.color)
        return best_move
