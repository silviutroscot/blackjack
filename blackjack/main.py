import getpass

from blackjack import gameUtils
from blackjack import api
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

# interface for registering a new player
def registerUser():
    username = input("Please insert your username:")
    password = getpass.getpass("Password: ")
    print(api.registerUser(username, password))

# interface for authenticating a player
def login():
    username = input("Please insert your username: ")
    password = getpass.getpass("Password: ")
    loginResponse = api.login(username, password)
    if loginResponse[0] == 0:
        credit = loginResponse[1]
        if (credit > 0):
            print ('''Welcome {username}, your current credit is {credit}\
            '''.format(username=username, credit=credit))
            startGameRound(username, credit)
        else: 
            print("You have insufficient founds; please top up your account")

# one round of the game
def startGameRound(username, credit): 
    # TODO: error handling
    bet = int(input("Please insert your bet (numerical value): "))
    if bet > credit: 
        print("You cannot bet more than your current sold; please try again")
        startGameRound(username, credit) 
    else: 
        deck = gameUtils.Deck() 
        dealer = [deck.getNextCard().value.value]
        dealer.append(deck.getNextCard().value.value) 
        hand = (deck.getNextCard().value.value, deck.getNextCard().value.value)
        sum = playerSum(hand)

# handler for the gameplay of a player in one game round
def playerSum(hand): 
    # count how many aces in hand
    playerAces = 0
    for card in hand:
        if card.value.value == 1:
            playerAces += 1
    print(playerAces)
    # compute the sum for each ace as having value 11, and decrease the 
    # value to 1, one by one, until the sum is smaller than 21 
    sum = 0 
    for card in hand: 
        # cards with value larger than 10 value 10
        value = card.value.value
        if card.value.value > 10:
            value = 10
        sum += value
    
    sum += playerAces*10
    while sum > 21 and playerAces > 0:
        sum -= 10
        playerAces -= 1
    
    return sum



if __name__ == "__main__": 
    api.initDatabase() 
    deck = gameUtils.Deck()
    print(deck.getNextCard().value.value) 
    initGame()
    #print(api.login("silviu", "parola1"))
