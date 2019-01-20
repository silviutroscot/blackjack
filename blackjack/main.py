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
    registrationResult = api.registerUser(username, password)
    print(registrationResult[1])
    if (registrationResult[0] == 0):
        startGameRound(username, api.kINITIAL_CREDIT)

# interface for authenticating a player
def login():
    username = input("Please insert your username: ")
    password = getpass.getpass("Password: ")
    loginResponse = api.login(username, password)
    if loginResponse[0] == 0:
        credit = loginResponse[1]
        if (credit > 0):
            print ('''Welcome {username}'''.format(username=username))
            startGameRound(username, credit)
        else: 
            print("You have insufficient founds; please top up your account")
    else:
        print(loginResponse[1])

# one round of the game
def startGameRound(username, credit): 
    print ('''Your current credit is {credit}'''.format(credit=credit))
    betInput = input("Please insert your bet (numerical value): ")
    bet = 0
    try:
        bet = int(betInput)
    except ValueError:
        print("Your bet needs to be an integer")
        startGameRound(username, credit)

    if bet > credit: 
        print("You cannot bet more than your current sold; please try again")
        startGameRound(username, credit)
    elif bet <= 0:
        print("Your bet needs to be at least 1")
        startGameRound(username, credit)
    else: 
        deck = gameUtils.Deck() 
        dealer = [deck.getNextCard().value.value]
        dealer.append(deck.getNextCard().value.value)
        print('''Dealer's hand: {card} and an unrevealed card'''.format(card=dealer[0]))
        hand = [deck.getNextCard().value.value, deck.getNextCard().value.value]
        
        applyPlayerDecision(deck, hand)
        pSum = playerSum(hand)
        # a sum larger than 21 makes the player lose automatically
        if pSum > 21:
            lostBet = -1 * bet
            newCredit = api.updateAccountCredit(username, credit, lostBet)
            api.showHand(hand)
            print("Sorry, you are busted :(")
            # if there was not one line modified, there is an error with db
            if newCredit[0] is not 1:
                print("An unexpected error occured. Please report it")
                exit()
            else:  
                startGameRound(username, newCredit[1])
        # a sum smaller than 21 plays the game. Now the dealer needs to play
        else:
            dealerValue = dealerSum(deck, dealer)
            # if the dealer has more than 21 it loses
            if dealerValue > 21:
                print("Dealer busted! You won!\n")
                newCredit = api.updateAccountCredit(username, credit, bet)
                if newCredit[0] is not 1:
                    print("An unexpected error occured. Please report it")
                    exit()
                else:  
                    startGameRound(username, newCredit[1])
            # if the dealer has less than the player loses
            elif dealerValue < pSum:
                print('''You have {pSum} and the dealer has {dealer}. You won!
                '''.format(pSum=pSum, dealer=dealerValue))
                newCredit = api.updateAccountCredit(username, credit, bet)
                if newCredit[0] is not 1:
                    print("An unexpected error occured. Please report it")
                    exit()
                else:  
                    startGameRound(username, newCredit[1])
            # if player`s sum and dealer`s sum are equal, the bet is returned
            elif dealerValue == pSum:
                print(("You have {pSum} and the dealer has {dealer}."
                " It's a draw.\n").format(pSum=pSum, dealer=dealerValue))
                startGameRound(username, credit)
            # if the dealer's sum is larger than the player's sum, player loses
            else:
                print('''You have {pSum}, the dealer has {dealer}. You lost:(
                '''.format(pSum=pSum, dealer=dealerValue))
                lostBet = -1 * bet
                newCredit = api.updateAccountCredit(username, credit, lostBet)
                if newCredit[0] is not 1:
                    print("An unexpected error occured. Please report it")
                    exit()
                else:  
                    startGameRound(username, newCredit[1])

# handler for the gameplay of a player in one game round
def playerSum(hand): 
    # count how many aces in hand
    playerAces = 0
    for card in hand:
        if card == 1:
            playerAces += 1

    # compute the sum for each ace as having value 11, and decrease the 
    # value to 1, one by one, until the sum is smaller than 21 
    sum = 0 
    for card in hand: 
        # cards with value larger than 10 value 10
        value = card
        if card > 10:
            value = 10
        sum += value
    
    sum += playerAces*10
    while sum > 21 and playerAces > 0:
        sum -= 10
        playerAces -= 1

    return sum


# method to handle user decision of drawing a card or to stop drawing
# Returns 'd' if user wants to draw and 's' if user wants to stop
def applyPlayerDecision(deck, hand):
    api.showHand(hand)
    sum = playerSum(hand)
    print('''The value of your hand is {value}'''.format(value=sum))
    playerDecisionRequest =  "Press 'd' to draw another card or 's' to stop: "
    playerDecision = input(playerDecisionRequest)
    if playerDecision is 'd':
        hand.append(deck.getNextCard().value.value)
        updatedSum = playerSum(hand)
        if updatedSum > 21:
            return 
        else:
            applyPlayerDecision(deck, hand)
    elif playerDecision is 's':
        return 
    else:
        print("Invalid key pressed")
        applyPlayerDecision(deck, hand)

def dealerSum(deck, hand):
    print('''Dealer's hand is: {cards}.'''.format(cards=hand))
    # count how many aces in hand
    dealerAces = 0
    for card in hand:
        if card == 1:
            dealerAces += 1

    # compute the sum for each ace as having value 11, and decrease the 
    # value to 1, one by one, until the sum is smaller than 21 
    sum = 0 
    for card in hand: 
        # cards with value larger than 10 value 10
        value = card
        if card > 10:
            value = 10
        sum += value
    
    sum += dealerAces*10
    while sum > 21 and dealerAces > 0:
        sum -= 10
        dealerAces -= 1
    
    # if the dealer has more than 17 in hand, it should stop playing
    if sum > 16:
        return sum
    else:
        hand.append(deck.getNextCard().value.value)
        return dealerSum(deck, hand)

if __name__ == "__main__": 
    api.initDatabase() 
    deck = gameUtils.Deck()
    initGame()
