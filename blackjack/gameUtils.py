from enum import Enum
import random

# enum representing the 4 possible symbols of a card
class SuitSymbols(Enum):
    club = "club"
    diamond = "diamond"
    heart = "heart"
    spade = "spade"

# enum for card values; for the purpose of this game
# the logic of handling the value of ace (1/11) is handled
# in the game engine
class Values(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    twelve = 12
    thirteen = 13
    fourteen = 14


# class representing a card from the deck
# each card has a value (e.g. 1, 2,..., 13(for Q), 14(for K))
# and a colour
class Card:
    def __init__(self, value, suitSymbol):
        self.value = value
        self.suit_symbol = suitSymbol

# class representing a standard 52 cards deck
# where each value occurs four times, one for each suit symbol

class Deck:
    def __init__(self):
        self.cards = []
        for value in Values:
            for suitSymbol in SuitSymbols:
                card = Card(value, suitSymbol)
                self.cards.append(card)

        self.shuffleDeck()

    def shuffleDeck(self):
        random.shuffle(self.cards)

    # return the next card in the deck and remove it
    def getNextCard(self):
        deckSize = len(self.cards)
        nextCard = self.cards[deckSize - 1]
        del self.cards[deckSize - 1]
        return nextCard
