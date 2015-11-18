from deuces.deuces import Card as dCard

class Card(object):
    def __init__(self, card_string):
        self.card_string = card_string

        self.number = '23456789TJQKA'.find(card_string[0])+2
        self.suit = card_string[1]
        self.rank = dCard.new(card_string)
