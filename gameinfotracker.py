from player import Player
from table import Table
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


    def update_settings(self, key, value):
        '''
        Updates game settings
        '''
        if key == 'table':
            self.table.parseHand(value)
        elif key == 'amountToCall':
            self.amount_to_call = int(value)
        else:
            if key == 'round':
                self.new_match()
            self.settings[key] = value


    def update_game_state(self, player, info_type, info_value):
        '''
        Updates game state
        '''
        # Checks if info pertains self
        if player == self.settings['your_bot']:
            self.log.debug("  INFOTYPE: " + info_type)
            # Update bot stack
            if info_type == 'stack':
                self.player.stack = int(info_value)
            # Remove blind from stack
            elif info_type == 'post':
                self.player.stack-= int(info_value)
            # Update bot cards
            elif info_type == 'hand':
                self.player.parseHand(info_value)
            else:
                stderr.write('Unknown info_type: %s\n' % (info_type))
                self.log.debug('Unknown info_type: %s\n' % (info_type))
        else:
            self.log.debug("  INFOTYPE: " + info_type)

            # Update opponent stack
            if info_type == 'stack':
                self.other_player.stack = int(info_value)

            # Remove blind from opponent stack
            elif info_type == 'post':
                self.other_player.stack -= int(info_value)

            # Opponent hand on showdown, currently unused
            elif info_type == 'hand':
                self.log.debug("SET HAND")
                self.other_player.parseHand(info_value)
            else:
                stderr.write('Unknown info_type: %s\n' % (info_type))
                self.log.debug('Unknown info_type: %s\n' % (info_type))

    def new_match(self):
        for k in self.spentPerStage:
            self.spentPerStage[k] = 0
        self.player = Player()
        self.other_player = Player()
        self.table = Table()
