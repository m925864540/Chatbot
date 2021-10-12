# Chatbot

## Description
- A simple chatbot that user can communicates to and xpects to get a response back. The chatbox are also able to return the current stock price when users enter the correct stock symbol

## Screenshots
- ![](./images/Picture1.png)
- ![](./images/Picture2.png)

## How to run the program
- Clone the repository
- Need to manually modify one file function cause by python version. Inside \venv\Lib\site-packages\sqlalchemy\util, open the file called compat, change the time_func = time.clock to time_func = time.perf_counter()

