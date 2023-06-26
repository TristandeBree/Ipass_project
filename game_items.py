from Card import Card
import random
def generate_cards():
    """
    generates all possible cards for this game
    :return: a list of cards
    """
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    numbers = ['7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    cards = []

    for suit in suits:
        for number in numbers:
            cards.append(Card(suit, number))

    return cards


def generate_4_cards(cards):
    """
    generates 4 random cards form the card-deck given
    :param cards: the card-deck given form which you can generate the cards
    :return: the 4 randomly generated cards that are all unique
    """
    no_copies = []
    for i in range(4):
        card = random.choice(cards)
        while card in no_copies:
            card = random.choice(cards)
        no_copies.append(card)
    return list(no_copies)