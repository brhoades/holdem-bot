from deuces.deuces import Card as dCard
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

    def getHand(self):
        '''
        get a hand compatible with deuces
        '''
        return [dCard.new(x.card_string) for x in self.hand]

    def getHumanHand(self):
        '''borkd'''
        return ' '.join([dCard.int_to_pretty_str(x) for x in self.getHand()])

    def getPrintableHand(self):
        return ' '.join([x.card_string for x in self.hand])
