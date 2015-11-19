# Heads Up Texas Hold'em Challenge bot
# Based on the Heads Up Omaha Challange - Starter Bot by Jackie <jackie@starapple.nl>
# Last update: 22 May, 2014
# @author Chris Parlette <cparlette@gmail.com> 
# @version 1.0 
# @license MIT License (http://opensource.org/licenses/MIT)

from sys import stderr, stdin, stdout
import os
import logging
import logging.handlers
from deuces.deuces import Card, Evaluator
import argparse
import json
from gameinfotracker import GameInfoTracker

class AI(GameInfoTracker):
    '''
    Main bot class
    '''
    def __init__(self, args):
        '''
        Bot constructor

        Add data that needs to be persisted between rounds here.
        '''
        self.ev = Evaluator()

        self.config =  json.load(args.config)
        LOG_FILENAME = self.config["logfile"]

        super(AI, self).__init__()

        # Set up a specific logger with our desired output level
        self.log = logging.getLogger('MyLogger')
        self.log.setLevel(logging.DEBUG)

        if args.log:
            self.handler = logging.handlers.RotatingFileHandler(
                    LOG_FILENAME, backupCount=5)
        else:
            self.handler = logging.StreamHandler(stderr)

        self.log.addHandler(self.handler)

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

                if command == 'settings' or command == 'match':
                    self.update_settings(parts[1], parts[2])
                    pass
                elif command.startswith('player'):
                    self.update_game_state(parts[0], parts[1], parts[2])
                    pass
                elif command == 'action':
                    totalsize = len(self.table.hand) + len(self.player.hand)
                    self.log.debug("ACTION: totalsize={0}".format(totalsize))
                    self.log.debug('  Table: ' + self.table.getHumanHand())
                    self.log.debug('  Us: ' + self.player.getHumanHand())
                    self.log.debug('  them: ' + self.other_player.getHumanHand())

                    back = None
                    if totalsize == 2: 
                        back = self.turn(parts[2], "pre_flop") + '\n'
                    elif totalsize == 5:
                        back = self.turn(parts[2], "flop") + '\n'
                    elif totalsize == 6:
                        back = self.turn(parts[2], "turn") + '\n'
                    elif totalsize == 7:
                        back = self.turn(parts[2], "river") + '\n'
                    else:
                        self.log.debug('Unknown stage!')
                        pass
                    self.log.debug('OUT: ' + str(back) + '\n')
                    stdout.write(back)
                    stdout.flush()
                else:
                    stderr.write('Unknown command: %s\n' % (command))
                    self.log.debug('ERR: Unknown command: %s\n' % (command))
                    stderr.flush()
            except EOFError:
                return

    def turn(self, timeout, stage):
        '''
        Once the turn is out, action is to us
        '''
        ours   = None
        action = "call"
        stagec = self.config[stage]
        amount = self.amount_to_call
        if len(self.table.hand) > 0:
            ours = self.get_score()
            

        self.log.debug("")
        self.log.debug("STAGE: " + stage)
        self.log.debug("")
        self.log.debug("Our score: " + str(ours))

        if stage == "pre_flop":
            # if we have a high pair or a high matching suit, raise
            if self.player.hand[0].number == self.player.hand[1].number or\
                (self.player.hand[0].suit == self.player.hand[1].suit and \
                self.player.hand[0].number > 10 and self.player.hand[1].number > 10):
                action = "raise"
                amount = stagec["raise_multiplier"] * self.player.stack
                return self.raise_amount(amount, stage)
            return '{0} {1}'.format(action, amount)

        if ours < stagec["raise_threshold"]:
            action = "raise"
            amount = stagec["raise_threshold"] / ours * stagec["raise_multiplier"] \
                * self.player.stack
            return self.raise_amount(amount, stage)

        if stagec['fold_threshold'] < ours:
            action = "fold"


        self.spentPerStage[stage] += amount
        return '{0} {1}'.format(action, amount)

    def raise_amount(self, amount, stage):
        # the raise amount is what the bot "thinks" we should be calling.
        if self.amount_to_call >= amount or self.player.stack < amount:
            return "call 0"
        
        self.spentPerStage[stage] += amount
        return '{0} {1}'.format("raise", amount)
    
    def get_score(self):
        base_score = self.ev.evaluate(self.table.getHand(), self.player.getHand())
        return base_score

if __name__ == '__main__':
    '''
    Not used as module, so run
    '''
    # get script directory for json file
    p = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")

    parser = argparse.ArgumentParser(description="Texas Holdem Bot.")
    parser.add_argument('--config', type=argparse.FileType('r', 0), default=p)
    parser.add_argument('--log', default=False, action='store_true')
    args = parser.parse_args()

    b = AI(args)
    try:
        b.run()
    except Exception:
        b.log.exception('ERROR')

