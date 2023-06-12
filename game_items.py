def generate_cards():
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    numbers = ['7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    cards = []

    for suit in suits:
        for number in numbers:
            cards.append(f'{number}_of_{suit}.png')

    return cards
