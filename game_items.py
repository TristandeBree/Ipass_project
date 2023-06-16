from Card import Card
import random
def generate_cards():
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    numbers = ['7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    cards = []

    for suit in suits:
        for number in numbers:
            cards.append(Card(suit, number))

    return cards


def generate_4_cards(cards):
    no_copies = []
    for i in range(4):
        card = random.choice(cards)
        while card in no_copies:
            card = random.choice(cards)
        no_copies.append(card)
    return list(no_copies)