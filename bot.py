# Heads Up Texas Hold'em Challenge bot
# Based on the Heads Up Omaha Challange - Starter Bot by Jackie <jackie@starapple.nl>
# Last update: 22 May, 2014
# @author Chris Parlette <cparlette@gmail.com> 
# @version 1.0 
# @license MIT License (http://opensource.org/licenses/MIT)

from sys import stderr, stdin, stdout
from player import Player
from table import Table
import logging
import logging.handlers
from deuces.deuces import Card, Evaluator
import random

class Bot(object):
    '''
    Main bot class
    '''
    def __init__(self):
        '''
        Bot constructor

        Add data that needs to be persisted between rounds here.
        '''
        self.settings = {}
        self.match_settings = {}
        self.game_state = {}
        self.player = Player()
        self.other_player = Player()
        self.table = Table()
        self.ev = Evaluator()

        self.id = random.getrandbits(4)

        LOG_FILENAME = 'logging%i.out' % self.id

        # Set up a specific logger with our desired output level
        self.log = logging.getLogger('MyLogger')
        self.log.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        self.handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, backupCount=5)
        self.log.addHandler(self.handler)



        ### These should be read from a configfile
        #
        # Percent of earnings to bet relative to confidence
        self._preflopBetRatio = 0.05
        self._flopBetRatio    = 0.15
        self._turnBetRatio    = 0.10
        self._riverBetratio   = 0.10

    def run(self):
        '''
        Main loop

        Keeps running while begin fed data from stdin.
        Writes output to stdout, remember to flush.
        '''
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                # End of file check
                if len(rawline) == 0:
                    break

                line = rawline.strip()

                # Empty lines can be ignored
                if len(line) == 0:
                    continue

                parts = line.split()
                command = parts[0].lower()
                self.log.debug('INCOMING:\t %s' % (line))

                if command == 'settings':
                    self.update_settings(parts[1:])
                    self.log.debug('SETTINGS RECIEVED')
                    pass
                elif command == 'match':
                    if parts[1] == 'table':
                        self.table.parseHand(parts[2])
                    else:
                        self.update_match_info(parts[1:])
                    self.log.debug('MATCH RECEIVED')
                    pass
                elif command.startswith('player'):
                    self.update_game_state(parts[0], parts[1], parts[2])
                    self.log.debug('PLAYER RECIEVED')
                    pass
                elif command == 'action':
                    totalsize = len(self.table.hand) + len(self.other_player.hand) \
                            + len(self.player.hand)
                    self.log.debug("ACTION: totalsize={0}".format(totalsize))
                    if totalsize == 2: 
                        self.log.debug("PREFLOP")
                        back = self.preflop(parts[2]) + '\n'
                        stdout.write(back)
                        self.log.debug('OUT: ' + back)
                        stdout.flush()
                        pass
                    elif totalsize == 5:
                        self.log.debug("FLOP")
                        back = self.flop(parts[2]) + '\n'
                        stdout.write(back)
                        self.log.debug('OUT: ' + back + '\n')
                        stdout.flush()
                        pass
                    elif totalsize == 13:
                        self.log.debug("TURN")
                        back = self.turn(parts[2]) + '\n'
                        stdout.write(back)
                        self.log.debug('OUT: ' + back)
                        stdout.flush()
                        pass
                    elif totalsize == 16:
                        self.log.debug("RIVER")
                        back = self.river(parts[2]) 
                        stdout.write(back + '\n')
                        self.log.debug('OUT: ' + back + '\n')
                        stdout.flush()
                        pass
                else:
                    stderr.write('Unknown command: %s\n' % (command))
                    self.log.debug('ERR: Unknown command: %s\n' % (command))
                    stderr.flush()
            except EOFError:
                return

    def update_settings(self, options):
        '''
        Updates game settings
        '''
        key, value = options
        self.settings[key] = value

    def update_match_info(self, options):
        '''
        Updates match information
        '''
        key, value = options

        if key == 'maxWinPot':
            value = int(value)
        self.match_settings[key] = value

    def update_game_state(self, player, info_type, info_value):
        '''
        Updates game state
        '''
        # Checks if info pertains self
        if player == self.settings['your_bot']:
            self.log.debug("  ME: " + player)
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

            # Round winnings, currently unused
            elif info_type == 'wins':
                if 'table' in self.match_settings:
                    del self.match_settings['table']

            else:
                stderr.write('Unknown info_type: %s\n' % (info_type))
                self.log.debug('Unknown info_type: %s\n' % (info_type))

        else:
            self.log.debug("  THEM: " + player)
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

            # Opponent round winnings, currently unused
            elif info_type == 'wins':
                if 'table' in self.match_settings:
                    del self.match_settings['table']
            else:
                stderr.write('Unknown info_type: %s\n' % (info_type))
                self.log.debug('Unknown info_type: %s\n' % (info_type))


    def preflop(self, timeout):
        '''
        Handle preflop hand possibilities
        '''
        self.log.debug(self.player.hand)
        card1 = self.player.hand[0]
        card2 = self.player.hand[1]

        raiseAmount = 0

        #pocket pair
        if card1.number == card2.number:
            raiseAmount = self.match_settings['maxWinPot']*self._preflopBetRatio
        
        #both face cards
        elif card1.number > 8 and card2.number > 8:
            raiseAmount = self.match_settings['maxWinPot']*self._preflopBetRatio
        
        #suited connectors
        elif card1.suit == card2.suit and abs(card1.number - card2.number) == 1:
            raiseAmount = self.match_settings['maxWinPot']*self._preflopBetRatio

        #suited ace
        elif card1.suit == card2.suit and (card1.number == 12 or card2.number == 12):
            raiseAmount = self.match_settings['maxWinPot']*self._preflopBetRatio

        elif int(self.match_settings['amountToCall']) == 0:
            return 'check 0'
        elif int(self.match_settings['amountToCall']) < int(self.match_settings['bigBlind']):
            return 'call 0'
        else:
            return 'fold 0'

        return 'raise {0}'.format(raiseAmount)


    def flop(self, timeout):
        '''
        Once the flop is out, action is to us
        '''
        self.log.debug('  Table: ' + self.table.getHumanHand())
        self.log.debug('  Us: ' + self.player.getHumanHand())
        self.log.debug('  them: ' + self.other_player.getHumanHand())
        score = self.ev.evaluate(self.table.getHand(), self.player.getHand())
        self.log.debug('  SCORE: ' + str(score))

        #made hand
        if int(ranking[0]) > 1:
            #already have 2pair or better, bet the pot
            return 'raise {0}'.format(self.match_settings['maxWinPot'])

        #flush draw
        flush_draw = False
        suits = ""
        for card in available_cards:
            suits += card.suit
        for card in available_cards:
            if suits.count(card.suit) > 3:
                flush_draw = True
        if flush_draw:
            return 'raise ' + str(int(self.match_settings['maxWinPot']) / 2)

        #straight draw
        values = sorted(['23456789TJQKA'.find(card.value) for card in available_cards])
        #check cards 0-3
        straight_draw = all(values[i] == values[0] + i for i in range(4))
        #check if we have A-4
        if not straight_draw:
            straight_draw = all(values[i] == values[0] + i for i in range(3)) and values[4] == 12
        #check cards 1-4
        if not straight_draw:
            straight_draw = all(values[i+1] == values[1] + i for i in range(4))
        if straight_draw:
            return 'raise ' + str(int(self.match_settings['maxWinPot']) / 2)

        #pair or ace high
        if int(ranking[0]) == 1 or values[4] == 12:
            if int(self.match_settings['amountToCall']) < (3 * int(self.match_settings['bigBlind'])) and int(self.match_settings['amountToCall']) > 0:
                return 'call 0'

        if int(self.match_settings['amountToCall']) == 0:
            return 'check 0'
        else:
            return 'fold 0'


    def turn(self, timeout):
        '''
        Once the turn is out, action is to us
        '''
        s = self.ev.evaluate(self.table.hand, self.player.hand)
        self.log.debug("EVAL: " + s)
        return 'call 0'
        for five_cards in combinations(available_cards, 5):
            if not ranking:
                ranking = self.ranker.rank_five_cards(available_cards)
            else:
                temp_ranking = self.ranker.rank_five_cards(available_cards)
                if int(temp_ranking[0]) > int(ranking[0]):
                    ranking = temp_ranking

        #made hand
        if int(ranking[0]) > 1:
            #already have 2pair or better, bet the pot
            return 'raise ' + str(int(self.match_settings['maxWinPot']))

        #flush draw
        flush_draw = False
        suits = ""
        for card in available_cards:
            suits += card.suit
        for card in available_cards:
            if suits.count(card.suit) > 3:
                flush_draw = True
        if flush_draw:
            return 'call 0'

        #straight draw
        values = sorted(['23456789TJQKA'.find(card.value) for card in available_cards])
        #check cards 0-3
        straight_draw = all(values[i] == values[0] + i for i in range(4))
        #check if we have A-4
        if not straight_draw:
            straight_draw = all(values[i] == values[0] + i for i in range(3)) and values[4] == 12
        #check cards 1-4
        if not straight_draw:
            straight_draw = all(values[i+1] == values[1] + i for i in range(4))
        #check cards 2-5
        if not straight_draw:
            straight_draw = all(values[i+2] == values[2] + i for i in range(4))
        if straight_draw:
            return 'call 0'

        #pair or ace high
        if int(ranking[0]) == 1 or values[4] == 12:
            if int(self.match_settings['amountToCall']) < (3 * int(self.match_settings['bigBlind'])) and int(self.match_settings['amountToCall']) > 0:
                return 'call 0'

        if int(self.match_settings['amountToCall']) == 0:
            return 'check 0'
        else:
            return 'fold 0'

    def river(self, timeout):
        '''
        Once the flop is out, action is to us
        '''
        
        self.log.debug("RIVER")
        self.log.debug(self.table.hand)
        s = self.ev.evaluate(self.table.hand, self.player.hand)
        self.log.debug("EVAL: " + s)

        #made hand
        #if int(ranking[0]) > 1:
        #    #already have 2pair or better, bet the pot
        #    return 'raise ' + str(int(self.match_settings['maxWinPot']))
        #elif int(self.match_settings['amountToCall']) == 0:
        #    return 'check 0'
        #else:
        return 'fold 0'

if __name__ == '__main__':
    '''
    Not used as module, so run
    '''
    b = Bot()
    try:
        b.run()
    except Exception:
        b.log.exception('ERROR')
