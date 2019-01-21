import unittest
from blackjack import gameUtils
from blackjack import main
class TestPlayerSum(unittest.TestCase):

    def testTwoNotAceCardsSum(self):
        three = gameUtils.Values.three
        threeCard = gameUtils.Card(three, gameUtils.SuitSymbols.club)
        eight = gameUtils.Values.eight
        eightCard = gameUtils.Card(eight, gameUtils.SuitSymbols.club)
        hand = [threeCard.value.value, eightCard.value.value]
        reversedHand = [eightCard.value.value, threeCard.value.value]
        self.assertEqual(main.playerSum(hand), 11)
        self.assertEqual(main.playerSum(reversedHand), 11)

    def testTwoCardsOneLargerThanTenNotAceSum(self):
        twelve = gameUtils.Values.twelve
        twelveCard = gameUtils.Card(twelve, gameUtils.SuitSymbols.club)
        nine = gameUtils.Values.nine
        nineCard = gameUtils.Card(nine, gameUtils.SuitSymbols.heart)
        hand = [twelveCard.value.value, nineCard.value.value]
        reversedHand = [nineCard.value.value, twelveCard.value.value]
        self.assertEqual(main.playerSum(hand), 19)
        self.assertEqual(main.playerSum(reversedHand), 19)

    def testThreeCardsNoAces(self):
        thirteen = gameUtils.Values.thirteen
        thirteenCard = gameUtils.Card(thirteen, gameUtils.SuitSymbols.club)
        nine = gameUtils.Values.nine
        nineCard = gameUtils.Card(nine, gameUtils.SuitSymbols.heart)
        four = gameUtils.Values.four
        fourCard = gameUtils.Card(four, gameUtils.SuitSymbols.heart)
        hand = [thirteenCard.value.value, nineCard.value.value]
        hand.append(fourCard.value.value)
        self.assertEqual(main.playerSum(hand), 23)

    def testTwoAces(self):
        one = gameUtils.Values.one
        ace = gameUtils.Card(one, gameUtils.SuitSymbols.heart)
        hand = [ace.value.value, ace.value.value]
        self.assertEqual(main.playerSum(hand), 12)

    def testCardAndAce(self):
        one = gameUtils.Values.one
        ace = gameUtils.Card(one, gameUtils.SuitSymbols.heart)
        thirteen = gameUtils.Values.thirteen
        thirteenCard = gameUtils.Card(thirteen, gameUtils.SuitSymbols.club)
        hand = [ace.value.value, thirteenCard.value.value]
        self.assertEqual(main.playerSum(hand), 21)
        nine = gameUtils.Values.nine
        nineCard = gameUtils.Card(nine, gameUtils.SuitSymbols.heart)
        secondHand = [ace.value.value, nineCard.value.value]
        self.assertEqual(main.playerSum(secondHand), 20)

    def testCardAndTwoAces(self):
        one = gameUtils.Values.one
        ace = gameUtils.Card(one, gameUtils.SuitSymbols.heart)
        ten = gameUtils.Values.ten
        tenCard = gameUtils.Card(ten, gameUtils.SuitSymbols.club)
        hand = [ace.value.value, tenCard.value.value, ace.value.value]
        self.assertEqual(main.playerSum(hand), 12)


if __name__ == '__main__':
    unittest.main()
