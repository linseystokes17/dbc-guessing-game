# dependencies
import os, sys # lets you have operating system tools
import random
import tkinter as tk

# guessing game refactored with tkinter
# Top level window
frame = tk.Tk()
frame.title("Guessing Game")
frame.geometry('200x200')
# Function for getting Input from textbox and printing it at label widget
  
def reset():
    global guesses, playing, win, complete, numGuesses, numWrongGuesses, maxGuesses, phrase, phrase_list, emptyPhrase
    guesses = []
    playing = True
    win = False
    complete = False
    numGuesses = 0
    numWrongGuesses=0
    maxGuesses = 7
    phrase = getPhrase(phrases, phrase_list)
    phrase_list.append(phrase)
    emptyPhrase = getPhraseBlank()

    lbl.config(text="Make a guess to begin")
    moveslbl.config(text = f'{maxGuesses-numWrongGuesses} wrong guesses left')
    lblError.config(text = "")
    phraselbl.config(text=getPhraseBlank())
    winslbl.config(text = f"Number of wins: {numWins}")
    playerlbl.config(text=f"It's player {currentPlayer}s turn")

    print(phrase)

def getPhraseBlank():
    emptyPhrase = []
    for i in range(0, len(phrase)):
        if phrase[i] in '., !\'':
            emptyPhrase.append(phrase[i])
        if phrase[i] in guesses:
            emptyPhrase.append(phrase[i])
        else:
            emptyPhrase.append('_')
    return emptyPhrase

def getPhrase(phrases, phrase_list):
    phraseIndex = random.randint(1, len(phrases))
    phrase = phrases[phraseIndex]
    while phrase in phrase_list:
        phraseIndex = random.randint(1, len(phrases))
        phrase = phrases[phraseIndex]
    return phrase

def makeGuess():
    global win, currentPlayer
    global numWins
    global numWrongGuesses
    global numGuesses
    inp = inputtxt.get(1.0, "end-1c")
    valid = checkGuess(inp, guesses, phrase)
    if maxGuesses == numWrongGuesses:
        moveslbl.config(text = f"You lost. Completed {numGuesses} moves")
        lblError.config(text = f"Try again")
        phraselbl.config(text=phrase)
        winslbl.config(text = f"Number of wins: {numWins}")
        
    elif valid:
        numGuesses+=1
        guesses.append(inp)
        guessesString = ','.join(guesses)
        lbl.config(text = f"Guesses: {guessesString}")
        phraselbl.config(text=getPhraseBlank())
        moveslbl.config(text=f'{maxGuesses-numWrongGuesses} wrong guesses left')
        playerlbl.config(text=f"It's player {currentPlayer}s turn")
    
    if inp == phrase or '_' not in getPhraseBlank():
        numWins+=1
        moveslbl.config(text = f"Player {currentPlayer} won! Completed in {numGuesses} moves")
        lblError.config(text = f"You guessed the correct word!")
        phraselbl.config(text=phrase)
        winslbl.config(text = f"Number of wins: {numWins}")

    inputtxt.delete("1.0","end")

def checkGuess(guess, guesses, phrase):
    global currentPlayer, player, numWrongGuesses
    if guess in guesses:
        lblError.config(text = "That has been guessed already, try again")
        inputtxt.delete("1.0","end")
        return False
    elif not guess.isalpha():
        lblError.config(text = "Please enter a letter")
        inputtxt.delete("1.0","end")
        return False
    elif guess not in phrase:
        if currentPlayer < players:
            currentPlayer+=1
        else:
            currentPlayer=1
        numWrongGuesses+=1
        inputtxt.delete("1.0","end")
        playerlbl.config(text=f"It's player {currentPlayer}s turn")
        lblError.config(text = "Not in the phrase")
        return True
    else:
        lblError.config(text = "In the phrase!")
        return True

# guessing game variables
f = open('english-words/words_alpha.txt', 'r')
global guesses, playing, win, complete, numGuesses, numWrongGuesses, maxGuesses, phrase, phrase_list, emptyPhrase, currentPlayer, players

phrases = []
players = 2
currentPlayer = 1
[phrases.append(line.strip('\n')) for line in f]
phrase_list = []
guesses = []
playing = True
win = False
complete = False
numGuesses = 0
numWrongGuesses=0
maxGuesses = 7
numWins = 0
guessesString=''
phrase = getPhrase(phrases, phrase_list)
phrase_list.append(phrase)
emptyPhrase = getPhraseBlank()
phrase = getPhrase(phrases, phrase_list)
phrase_list.append(phrase)
emptyPhrase = getPhraseBlank()
print(phrase)

# TextBox Creation
inputtxt = tk.Text(frame,
            height = 1,
            width = 25)
inputtxt.pack()
  
# Button Creation
guessButton = tk.Button(frame,
            text = "Guess", 
            command = makeGuess)
guessButton.pack()
  
# Label Creation
lbl = tk.Label(frame, text = f"Player {currentPlayer}, make a guess to begin")
lbl.pack()

lblError = tk.Label(frame, text = "")
lblError.pack()

phraselbl = tk.Label(frame, text = getPhraseBlank())
phraselbl.pack()

moveslbl = tk.Label(frame, text=f'{maxGuesses-numWrongGuesses} wrong guesses left')
moveslbl.pack()

winslbl = tk.Label(frame, text=f"Number of wins: {numWins}")
winslbl.pack()

playerlbl = tk.Label(frame, text=f"It's player {currentPlayer}s turn")
playerlbl.pack()

resetButton = tk.Button(frame,
            text = "Play Again", 
            command = reset)
resetButton.pack()

frame.mainloop()