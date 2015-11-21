from player import Player
from table import Table
from deck import Deck
from sys import stderr, stdin, stdout

class GameInfoTracker(object):
    def __init__(self):
        self.settings = {}
        self.game_state = {}
        self.spentPerStage = {"pre_flop": 0, "flop": 0, "turn": 0, "river": 0}

        self.amount_to_call = 0

        self.player = None
        self.other_player = None
        self.table = None
        self.deck = Deck()

        self.last_hand_count = 0
        self.last_hand_score = 0


    def update_settings(self, key, value):
        '''
        Updates game settings
        '''
        if key == 'table':
            self.table.parseHand(value)
            self.deck.remove_cards(self.table.hand)
        elif key == 'amountToCall':
            self.amount_to_call = int(value)
        else:
            if key == 'round':
                #self.log.debug("NEW ROUND: " + value)
                self.new_match()
            self.settings[key] = value


    def update_game_state(self, player, info_type, info_value):
        '''
        Updates game state
        '''
        # Checks if info pertains self
        if player == self.settings['your_bot']:
            # Update bot stack
            if info_type == 'stack':
                self.player.stack = int(info_value)
            # Remove blind from stack
            elif info_type == 'post':
                self.player.stack-= int(info_value)
            # Update bot cards
            elif info_type == 'hand':
                self.player.parseHand(info_value)
                self.deck.remove_cards(self.player.hand)
            elif info_type == 'win':
                pass
                #self.log.debug("I WIN!")
            else:
                pass
                #stderr.write('Unknown info_type: %s\n' % (info_type))
                #self.log.debug('Unknown info_type: %s\n' % (info_type))
        else:

            # Update opponent stack
            if info_type == 'stack':
                self.other_player.stack = int(info_value)

            # Remove blind from opponent stack
            elif info_type == 'post':
                self.other_player.stack -= int(info_value)

            # Opponent hand on showdown, currently unused
            elif info_type == 'hand':
                self.other_player.parseHand(info_value)
                self.deck.remove_cards(self.other_player.hand)
            elif info_type == 'wins':
                pass
                #self.log.debug("THEY WIN!")
            else:
                pass
                #stderr.write('Unknown info_type: %s\n' % (info_type))
                #self.log.debug('Unknown info_type: %s\n' % (info_type))

    def new_match(self):
        for k in self.spentPerStage:
            self.spentPerStage[k] = 0
        self.player = Player()
        self.other_player = Player()
        self.table = Table()
        self.deck = Deck()
        self.last_hand_count = 0
        self.last_hand_score = 0
