from Card import Card
class Player:
    def __init__(self, number, first, hand):
        self.number = number
        self.first = first
        self.hand = hand
        self.left = None
        self.right = None
        self.last = False

    def set_neighbours(self, left, right):
        if self.first:
            right.last = True
            self.right = right
            self.left = left
        else:
            self.right = right
            self.left = left

    def __str__(self):
        return f'Player: {self.number} has these cards: {self.hand} and these are his neighbours {self.left} and {self.right}'

