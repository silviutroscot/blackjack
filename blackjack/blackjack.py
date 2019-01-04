import api
import gameUtils
import getpass


# register a player

# the initialization of the game
def initGame():
    command = input("Press 'r' to register," 
    "'l' to login or 'q' to quit: ")
    if command is 'r':
        registerUser()
    elif command is 'l':
        login()
    else:
        print("Sorry, you typed an invalid character \n")

def registerUser():
    username = input("Please insert your username:")
    password = getpass.getpass("Password: ")
    print(api.registerUser(username, password))

def login():
    username = input("Please insert your username: ")
    password = getpass.getpass("Password: ")
    loginResponse = api.login(username, password)
    if loginResponse[0] == 0:
        credit = loginResponse[1]
        if (credit > 0):
            print ('''Welcome {username}, your current credit is {credit}\
            '''.format(username=username, credit=credit))


if __name__ == "__main__":
    api.initDatabase()
    deck = gameUtils.Deck()
    print(deck.getNextCard().value.value)
    initGame()
    #print(api.login("silviu", "parola1"))
        