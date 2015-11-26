class Deck(object):
    """
        our deck for counting cards
    """
    def __init__(self):
        suits  = "s h d c".split()
        numbers = "A K Q J T 9 8 7 6 5 4 3 2".split()

        self.cards = []

        # we start with all cards
        for s in suits:
            for n in numbers:
                self.cards.append(n+s)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def remove_cards(self, cards):
        '''
        Pass an array of Cards, they're removed from the deck.
        '''
        [self.remove_card(x.card_string) for x in cards]
