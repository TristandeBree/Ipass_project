class Card:

    def __init__(self, _suit, _number):
        self.suit = _suit
        self.number = _number

    def __str__(self):
        return f'{self.number}_of_{self.suit}'
