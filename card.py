from deuces.deuces import Card as dCard

class Card(object):
    def __init__(self, card_string):
        self.card_string = card_string
        self.number = card_string[1]
        self.suit = card_string[0]
        self.rank = dCard.new(card_string)
