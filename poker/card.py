from deuces.deuces import Card as dCard

class Card(object):
    def __init__(self, card_string):
        self.card_string = card_string

        suits  = "shdc"
        numbers = "AKQJT98765432"
        self.card_number = suits.find(card_string[1]) + numbers.find(card_string[0])*4+1
        # specialKEval ^ offset by one

        self.number = numbers[::-1].find(card_string[0])+2
        self.suit = card_string[1]
        self.rank = dCard.new(card_string)

