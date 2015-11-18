from card import Card

class CardHandler(object):
    def __init__(self):
        self.hand = []

    def setHand(self, hand):
        self.hand = hand

    def parseHand(self, hand):
        self.hand = self.parseCards(hand)

    def parseCards(self, cards_string):
        '''
        Parses string of cards and returns a list of Card objects
        '''
        return [Card(card) for card in cards_string[1:-1].split(',')]
