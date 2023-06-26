class Card:
    ranks = ["jack", "queen", "king", "ace", "7", "8", "9", "10"]
    def __init__(self, _suit, _number):
        self.suit = _suit
        self.number = _number

    def __str__(self):
        return f'{self.number}_of_{self.suit}'

    def __gt__(self, other):
        return self.ranks.index(self.number) > self.ranks.index(other.number)

    def __lt__(self, other):
        return self.ranks.index(self.number) < self.ranks.index(other.number)

    def __eq__(self, other):
        return self.ranks.index(self.number) == self.ranks.index(other.number) and self.suit == other.suit
