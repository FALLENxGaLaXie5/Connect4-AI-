#Joshua Steward - AI HW2 Connect 4 Game

from Connect4 import *

def main():

    print("Hello my name is Frankie! I will be beating you at Connect4 today. ")
    game = Game()
    game.printState()

    #check to see if game has been won
    done = False
    while not done:
        while not game.finished:
            #game makes a move based on if it's the player's or ai's turn
            game.nextMove()

        game.findFours()
        game.printState()


        while True:
            play_again = str(input("Would you like to play again? "))

            if play_again.lower() == 'y' or play_again.lower() == 'yes':
                game.createGame()
                game.printState()
                break
            else:
                print("Thanks for playing!")
                exit = True
                break

if __name__ == "__main__":
    main()