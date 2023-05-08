
counter = 0
while True:

    content = input("\n enter 'sell' for sell signal and buy for opposite \n")
    counter = counter + 1
    if (content == 'sell'):
        LOG_FILE_PATH = f'../inboxes/generated_signal{counter}.txt'
        logFile = open(LOG_FILE_PATH, 'x')
        logFile.write("this is a sell signal")
        logFile.close()
    if (content == 'buy'):
        LOG_FILE_PATH = '../inboxes/generated_signal.txt'
        logFile = open(LOG_FILE_PATH, 'x')
        logFile.write("this is a buy signal")
        logFile.close()
    else:
        print("command not supported !! try again")
