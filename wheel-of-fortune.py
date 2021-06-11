''' Pseudocode for wheel of fortune
- create the wheel (54 potential slots)
    twenty-four slots with the $1 symbol, 
    fifteen with the $2, 
    seven with the $5, 
    four with the $10, 
    two each for the $20 and the Joker ($40).
- read phrases.json file
- initialize variables
    - each player's winnings (array)
    - currentPlayer
    - list of guesses
    - randomly select a category / phrase as phrase

- display wheel
- display labels
    - category as hint 
    - blank phrase
    - current player
    - guesses used
    - current scores
- display buttons
    - submit guess
    - reset game

'''
# dependencies
import os, sys # lets you have operating system tools
import random
from tkinter import *
import json
import time

# load json
f = open('hangman_python/phrases.json',)
json_object = json.load(f)
categories = list(json_object.keys())

# Top level window
root = Tk()
root.title("Wheel of Fortune")
root.geometry('800x400')

main_frame = Frame(root)
wheel_frame = Frame(root)

wheel_frame.pack(side = RIGHT)
main_frame.pack(side = LEFT, padx=20)

# reset all variables to restart game
def reset():
    global guesses, numRounds, phrase, phrase_list, emptyPhrase
    guesses = []

    phrase = getPhrase(categories, phrase_list)
    phrase_list.append(phrase)
    emptyPhrase = getPhraseBlank(phrase)

    lblGuesses.config(text="Make a guess to begin")
    lblRounds.config(text = f'{numRounds} rounds left')
    lblError.config(text = "")
    lblPhrase.config(text=getPhraseBlank(phrase))
    lblPlayer.config(text=f"Player {currentPlayer}")

# generate blank array of phrase - COMPLETE
def getPhraseBlank(phrase):
    emptyPhrase = []
    for i in range(0, len(phrase)):
        if phrase[i] in '., !\'&%^*$#@();:-':
            emptyPhrase.append(phrase[i])
        elif phrase[i] in guesses:
            emptyPhrase.append(phrase[i])
        else:
            emptyPhrase.append('_')
    return ''.join(emptyPhrase)

# randomly select a phrase from random category - COMPLETE
def getPhrase(categories, phrase_list):
    randCat = categories[random.randint(0, len(categories)-1)]
    randCatPhrase = json_object[randCat][random.randint(0, len(json_object[randCat])-1)].lower()
    while randCatPhrase in phrase_list:
        randCat = categories[random.randint(0, len(categories))]
        randCatPhrase = json_object[randCat][random.randint(0, len(json_object[randCat]))].lower()
    
    print(f"Category: {randCat}, Phrase: {randCatPhrase}")
    return randCatPhrase

# prompt for input to make a new guess
def makeGuess():
    inp = inputtxt.get(1.0, "end-1c")
    valid = checkGuess(inp, guesses, phrase)
    checkWin(inp, phrase, valid)
    inputtxt.delete("1.0","end")

# check that guess is acceptable - TODO
def checkGuess(guess, guesses, phrase):
    global currentPlayer
    if len(guess) > 1 and guess!=phrase:
        lblError.config(text = "Guess is too long, try again")
        return False
    elif guess in guesses:
        lblError.config(text = "That has been guessed already, try again")
        return False
    elif not guess.isalpha():
        lblError.config(text = "Please enter a letter")
        return False
    elif guess not in phrase:
        if currentPlayer < players:
            currentPlayer+=1
        else:
            currentPlayer=1
        lblPlayer.config(text=f"Player {currentPlayer}")
        lblError.config(text = "Not in the phrase")
        return True
    else:
        lblError.config(text = "In the phrase!")
        return True

def checkWin(inp, phrase, valid):
    # determine state of game after guess
    global numRounds
    if valid:
        guesses.append(inp)
        guessesString = ','.join(guesses)
        lblGuesses.config(text = f"Guesses: {guessesString}")
        lblPhrase.config(text=getPhraseBlank(phrase))
        lblPlayer.config(text=f"Player {currentPlayer}")
    if inp == phrase or '_' not in getPhraseBlank(phrase):
        lblRounds.config(text = f"{numRounds} rounds left")
        lblError.config(text = f"Player {currentPlayer} guessed the correct word!")
        lblPhrase.config(text=phrase)

def drawWheel(wheelCanvas):
    coordinates =  20, 20, 300, 320
    incr = 360/54
    for i in range(0,54):
        if i%5==0:
            arc = wheelCanvas.create_arc(coordinates, start=i*incr, extent=incr, fill="red")
        else:
            arc = wheelCanvas.create_arc(coordinates, start=i*incr, extent=incr, fill="blue")

def rotate():
    global wheelVector
    wheelCanvas.delete()
    coordinates =  20, 20, 300, 320
    incr = 360/54
    for i in range(0,54):
        '''twenty-four slots with the $1 symbol, 
            fifteen with the $2, 
            seven with the $5, 
            four with the $10, 
            two each for the $20 and the Joker ($40).
        '''
        if i%5==0:
            arc = wheelCanvas.create_arc(coordinates, start=i*incr, extent=incr, fill="red")
        else:
            arc = wheelCanvas.create_arc(coordinates, start=i*incr, extent=incr, fill="blue")

def randomValue():
    
# initialize variables
players = 3
playerScores = []*players
currentPlayer = 1
phrase_list = []
guesses = []
wheelVector = 0

numRounds = 3

phrase = getPhrase(categories, phrase_list)
phrase_list.append(phrase)
emptyPhrase = getPhraseBlank(phrase)

lblPlayer = Label(main_frame, text=f"Player {currentPlayer}")
lblPlayer.pack()

# TextBox Creation
inputtxt = Text(main_frame,
            height = 1,
            width = 25)
inputtxt.pack()
  
# Button Creation
guessButton = Button(main_frame,
            text = "Guess", 
            command = makeGuess)
guessButton.pack()
  
# Label Creation
lblGuesses = Label(main_frame, text = f"Guesses: {guesses}")
lblGuesses.pack()

lblError = Label(main_frame, text = "")
lblError.pack()

lblPhrase = Label(main_frame, text = getPhraseBlank(phrase))
lblPhrase.pack()

lblRounds = Label(main_frame, text=f'{numRounds} rounds left')
lblRounds.pack()

# Button Creation
resetButton = Button(main_frame,
            text = "Play Again", 
            command = reset)
resetButton.pack()

wheelCanvas = Canvas(wheel_frame, bg='grey')
drawWheel(wheelCanvas)
wheelCanvas.pack() 

spinWheelButton = Button(wheel_frame, 
        text='Spin!',
        command = randomValue)
spinWheelButton.pack()

main_frame.mainloop()