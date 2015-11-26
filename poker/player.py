from cardhandler import CardHandler

class Player(CardHandler):
    def __init__(self):
        super(Player, self).__init__()
        self.stack = None

