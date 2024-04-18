# File: Wordle.py
# Alex Weirth

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_ROWS, N_COLS
import random

def wordle():

    '''
    Function that carries out the Wordle game. The user has 6 attempts to guess the random 5 letter word pulled from the WordleDictionary.py. Every 
    life, a letter guessed in the correct place with be highlighted green, a letter that is present in the word howver not placed with the correct 
    index will be highlighted as yellow, while a letter not in the word will be grey. The Wordle keyboard tracks letters guessed and marks them 
    with their correct color as well. If a word guessed is not in the WordleDictionary.py, the program will return "word not in list." If a 
    players gets the correct answer the game congratulates the user and asks the user to close the program.
    Arguments: The user passes in a series of strings typed into the Wordle interface using the keyboard and enter key.
    Returns: The function updates the graphics window.
    '''
    gw = WordleGWindow()
    ROW = 0
    gw.set_current_row(ROW)
    answer = random.choice(FIVE_LETTER_WORDS).upper()

    #MS1 - Display the random word
    def set_answer():
        for col in range(N_COLS):
            gw.set_square_label(ROW, col, answer[col])

    #MS2 - Enter action Function
    def enter_action():
        '''
        This function is executed in the event of the enter key being pressed on the keyboard or game graphics. The function gets the current row
        and iterates over the labels in each box for the current ROW. The function gets these characters and adds them one by one to the originally 
        empty string 'guess'. The function also checks to make sure the word is in the WordleDictionary list, and if it is not displays the message 
        'Word not in list'. Also checked is if the user guesses the correct answer, if so a winning message is displayed.
        Arguments: None, the function is executed in the event of an enter action.
        Returns: String 'Guess'
        '''
        ROW = gw.get_current_row()
        guess = ""
        column = 0
        for i in range(N_COLS):
            letter = gw.get_square_label(ROW, i)
            guess = guess + letter
            column += 1
        if guess.lower() in FIVE_LETTER_WORDS:
            color_user_guess(guess, ROW)
            next_row()
            if guess == answer:
                gw.show_message('You win! Close the window to play again.')
                gw.set_current_row(None)
            else:
                pass
        else:
            gw.show_message('Word not in list')
        return guess
            


    def next_row():
        '''
        This function is used within the enter action function to advance the game to the next row after the guess in the previous row is obtained.
        The function also tracks the ROW number and allows the user one final guess on their sixth attempt and after that displays a game over 
        message and informs the user of the correct answer.
        Arguments: None, the function is just called to advance the ROW variable if allowed.
        Returns: ROW, which is an int type
        '''
        ROW = gw.get_current_row()
        if ROW == 5:
            gw.show_message('You ran out of turns! The word was: ' + answer)
        else:
            ROW += 1
            gw.set_current_row(ROW)
            return ROW
       

    
    def color_user_guess(guess, ROW):
        '''
        This function takes string guess and the current row to color the boxes based on comparing the indexes and characters of both guess and answer
        to one another. The function also colors the WordleWindow keyboard to track letter guesses and correctness.
        Arguments: Passed in are the string guess, as well as integer ROW variable.
        Returns: Nothing, the state of the boxes in the ecurrent row and keys in the WordleWindow are left changed.
        '''
        for index, letter in enumerate(guess):
            state = "MISSING"
            key_color = "MISSING"
            for answer_index, answer_letter in enumerate(answer):
                if letter == answer_letter:
                    if index == answer_index:
                        state = "CORRECT"
                        key_color = "CORRECT"
                        break
                    else:
                        state = "PRESENT"
                        key_color = "PRESENT"
            ROW = gw.get_current_row()
            gw.set_square_state(ROW, index, state)
            gw.set_key_state(letter, key_color)
                
    ###The event listener that executes the enter_action function.###
    gw.add_enter_listener(enter_action)


if __name__ == "__main__":
    wordle()    