from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.logic import logic_adapter
# from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
import pytz
import re
from tkinter import *
import yfinance as yf
import sys
import os


#initialize a chatBot object
chatBotAI = ChatBot(name='ChatBotAI',
                    logic_adapters=[
                            'chatterbot.logic.BestMatch',
                            'chatterbot.logic.MathematicalEvaluation',
                    ],)

# Initialize a ChatterBotCorpusTrainer with our chatBotAI as the parameter.
# Then we can train our chatBot by using the corpus provided by chatterbot.
chatBotTrainer = ChatterBotCorpusTrainer(chatBotAI)
chatBotTrainer.train("chatterbot.corpus.english")

# This function get the response from the chatBotAI we created with user input as its parameter.
# The response will later appear in the GUI.
def chatBotResponse(userInput):
    return chatBotAI.get_response(userInput)


# Create Tkinter, GUI below.
root = Tk()
root.title('ChatBox')

# A area to display the chat.
# The background is light yellow, and its state is currently disabled so user can not click into it.
displayBox = Text(root, bg='light yellow')
displayBox.pack()
displayBox.insert(INSERT, 'ChatBot: Hello! We can chat here! We can talk about all sort of topic!\n')
displayBox.configure(state=DISABLED)

# Store user input.
userInput = StringVar()

# This is a box located at the bottom that allows user to enter text.
# There is a placeholder added, and fill till the x-axis.
inputBox = Entry(root, text=userInput)
inputBox.insert(0, 'Chat here!')  # Placeholder
inputBox.pack(side='bottom', fill='x')

# Fetch the user input from the inputBox by using inputBox.get(),
# perform check if the input is stock/stock related or just any random input.
# Then, insert it into the displayBox, and set the userInput to ''.
# Before inserting into displayBox, the state needs to change to normal and back to disabled after insert to prevent
# user clicking on it.
def displayMessage(event):
    displayBox.configure(state=NORMAL)
    displayBox.insert(INSERT, 'User: %s\n' % inputBox.get())

    # Called to isTicker() to do some processing with user response and see if it is stock related stuff.
    Ticks = isTicker(inputBox.get())
    # See which type of response we will get, a stock response, or a chatbot generated response.
    responseType(Ticks)

    userInput.set('')
    displayBox.configure(state=DISABLED)
    return "break"

# This function deletes the placeholder on inputBox once the user click on it.
def deletePlaceHolder(event):
    inputBox.delete(0, END)

# This function creates a list of words from the string to be searched and then a set of those words
def wordsInString(expectedWord, response):
    return set(expectedWord).intersection(response.split())

# Process the user response and check if the response is stock related or not.
def isTicker(userResponse):
    # Make the string only contains letters, space, and lowercase.
    response = re.sub(r'[^A-Za-z ]+', '', userResponse)
    response = response.lower()

    # A list of stock related word we expect to hear from user.
    expectedWord = ['stock', 'stocks', 'price', 'prices', 'ticker', 'tickers', 'stock market', 'market', 'markets']

    if wordsInString(expectedWord, response):
        # Check if user enter any stock related word, and if does, we prompt the user to enter only the symbol.
        return 'Yes, please enter just the ticker symbol(name) and I will gladly check that for you!'
    elif(' ' not in response and len(response) < 5):
        # Call to userTicker() when user enter a single word and is less than 5 letter because
        # ticker can have up to 4 letter(maybe stock symbol, or other stuff).
        return userTicker(response)
    else:
        # This case the user enter multiple words seperates with space, therefore we just return empty string.
        return ''

# Handle the elif statement in isTicker(), since a single word enter by users maybe a stock symbol or any
# other random word, we want to check what it is.
def userTicker(userTick):
    # Create a ticker first using the yfinance lib.
    ticker = yf.Ticker(userTick)
    latestPrice=''
    reString = ''

    # ticker.history() will return a message like this: "No data found for this date range, symbol may be delisted"
    # to the console if the symbol is not found, and unable to display it to the GUI.
    # So I put it in a try/catch.
    try:
        # Used to suppress the console output by ticker.history()
        old_stdout = sys.stdout  # backup current stdout
        sys.stdout = open(os.devnull, "w")
        # In this case, the stock is successfully found.
        latestPrice = ticker.history(period='1d')['Close'][0]

        sys.stdout = old_stdout  # reset old stdout

        if(isinstance(latestPrice, float)):
            reString = '%s price is: $%.2f' % (userTick, latestPrice)
    except:
        # In this case, the user enter ticker does not exist, that means the user is entering random stuff not
        # relateing to stock.
        reString=''

    return reString

# Based on the paramter Ticks, we will see if we want to return the stock price, or just a chatbot generated response.
def responseType(Ticks):
    # Depending on the result of Ticks, the following logic will be executes.
    if (len(Ticks) == 0):
        # response enter by user is not stock related, so we get the response from the chatBox, and display it.
        responseMessage = chatBotResponse(inputBox.get().lower())
        displayBox.insert(INSERT, 'ChatBot: %s\n' % responseMessage)
    else:
        # This case, the stock is founded, we display the stock and its current time price.
        displayBox.insert(INSERT, 'ChatBot: %s\n' % Ticks)


# Bind the deletePlaceHolder method so when user left click on the inputBox, the placeholder will be deleted.
inputBoxOnClick = inputBox.bind('<Button-1>', deletePlaceHolder)

# Bind the displayMessage method with inputBox so when user hits enter on the
# keyboard, it send the message.
inputBox.bind("<Return>", displayMessage)

root.mainloop()
