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
from deuces.deuces import Card as dCard, Evaluator
import argparse
import json
import itertools
import cProfile

from poker.card import Card
from poker.gameinfotracker import GameInfoTracker

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

        if args.config_data is None:
            self.config =  json.load(args.config)
        else:
            self.config = json.loads(args.config_data)
        LOG_FILENAME = self.config["logfile"]

        self.eval_path = [os.path.join(os.path.dirname(os.path.realpath(__file__)), "score", "eval")]

        super(AI, self).__init__()

        # Set up a specific logger with our desired output level
        self.log = logging.getLogger('MyLogger')
        self.log.setLevel(logging.DEBUG)

        if args.no_log:
            self.log.setLevel(logging.CRITICAL)
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
                self.log.debug("INCOMING:\t {0}".format(line))

                if command == 'settings' or command == 'match':
                    self.update_settings(parts[1], parts[2])
                    pass
                elif command.startswith('player'):
                    self.update_game_state(parts[0], parts[1], parts[2])
                    pass
                elif command == 'action':
                    totalsize = len(self.table.hand) + len(self.player.hand)
                    self.log.debug("ACTION: totalsize={0}".format(totalsize))
                    if self.log: # converting this to pretty hands is expensive enough to catch
                        self.log.debug("  Table: {0}".format(self.table.getHumanHand()))
                        self.log.debug("  Us:    {0}".format(self.player.getHumanHand()))

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
                        #self.log.debug('Unknown stage!')
                        pass
                    self.log.debug("OUT: {0}\n".format(back))
                    stdout.write(back)
                    stdout.flush()
                else:
                    stderr.write("Unknown command: %s\n".format(command))
                    self.log.debug("ERR: Unknown command: %s\n".format(command))
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
            ours = self.get_score(stagec)
            

        # check call amount
        if amount >= self.player.stack:
            # this strategy is annoying... so check if our hand is "good enough"
            if ours > self.config["max_stack_bet_threshold"]:
                return "call 0"
            return "fold 0"

        self.log.debug("")
        self.log.debug("")
        self.log.debug("STAGE: " + stage)
        self.log.debug("    Our score: " + str(ours))

        if stage == "pre_flop":
            # if we have a high pair or a high matching suit, raise
            if self.player.hand[0].number == self.player.hand[1].number or\
                self.player.hand[0].suit == self.player.hand[1].suit and \
                (self.player.hand[0].number > 10 and self.player.hand[1].number > 10):
                amount = stagec["raise_multiplier"] * self.player.stack
                return self.raise_amount(amount, stage)
            elif amount >= stagec["fold_amount_threshold"]:
                return "fold 0"
            return '{0} {1}'.format(action, amount)

        # check if call amount is higher than what we could possibly have
        if ours >= stagec["fold_threshold"]  \
            or self.get_raise(ours, stagec) < self.amount_to_call:
            return "fold 0"

        if ours >= stagec["raise_threshold"]:
            return self.raise_amount(self.get_raise(ours, stagec), stage)

        if ours < stagec['fold_threshold']:
            action = "fold"

        self.spentPerStage[stage] += amount
        return '{0} {1}'.format(action, amount)

    def get_raise(self, ours, stage_config):
        if ours < 1:
            return 0
        return(stage_config["raise_threshold"] \
            / ours * stage_config["raise_multiplier"])

    def raise_amount(self, amount, stage):
        if amount > self.player.stack:
            amount = self.player.stack

        if self.amount_to_call >= amount:
            return "call 0"

        amount -= self.spentPerStage[stage]

        if amount < self.minimum_raise:
            self.log.debug("Amount to raise ({0}) is below minimum".format(amount))
            return "call 0"

        self.spentPerStage[stage] += amount
        return '{0} {1}'.format("raise", amount)
    
    def get_score(self, stagec):
        """
        Returns a score that adjusts for their average hand.
        return > 0: our hand is better on average by #
        return < 0: our hand is worse on average by #
        """
        if self.last_hand_count == len(self.table.hand)+len(self.player.hand) or len(self.table.getHand()) == 0:
            return self.last_hand_score
        else:
            self.last_hand_count = len(self.table.hand) + len(self.player.hand)
        
        score = 0

        base_score = self.ev.evaluate(self.table.getHand(), self.player.getHand())
        table_adjusted = tuple(self.table.getHand())

        # change deck into deuces cards
        deck_adjusted = (dCard.new(x) for x in self.deck.cards)

        # all possbile hands
        possibilities = itertools.combinations(deck_adjusted, 2)

        length = len(self.table.hand) + len(self.player.hand)
        scoresum = 0
        num = 0
        for p in possibilities:
            scoresum += self.ev.hand_size_map[length](table_adjusted+p)
            num += 1
        scoresum /= float(num)
        # get our score adjusted for what they could have
        self.log.debug("  Base score:     {0}".format(base_score))
        self.log.debug("  Score average:  {0}".format(scoresum))
        self.log.debug("  Relative Score: {0}".format(base_score - scoresum))
        self.log.debug("  Confidence:     {0}".format(self.config["confidence"]))

        score = (base_score + stagec["score_offset"])
        self.log.debug("  Offset Score:   {0}".format(score))

        if score < 0:
            score /= self.config["confidence"]
        else:
            score *= self.config["confidence"]
        score -= scoresum 

        self.last_hand_score = score
        self.log.debug("  Score:          {0}".format(score))

        return score


if __name__ == '__main__':
    '''
    Not used as module, so run
    '''
    # get script directory for json file
    p = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")

    parser = argparse.ArgumentParser(description="Texas Holdem Bot.")
    parser.add_argument('--config', type=argparse.FileType('r', 0), default=p)
    parser.add_argument('--config-data', default=None)
    parser.add_argument('--log', default=False, action='store_true')
    parser.add_argument('--no-log', default=False, action='store_true')
    args = parser.parse_args()

    b = AI(args)
    try:
        b.run()
    except Exception:
        b.log.exception('ERROR')

