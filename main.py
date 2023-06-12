import pygame
import random
import game_items

# initiating pygame
pygame.init()

# making the screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

cards = game_items.generate_cards()

running = True
cards_given = False


def generate_cards():
    no_copies = set()
    for i in range(4):
        card = random.choice(cards)
        while card in no_copies:
            card = random.choice(cards)
        no_copies.add(card)
    return list(no_copies)


x = 600
y = 600
x2 = 100
y2 = 100
x3 = 1400

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill((0, 0, 0))

    if not cards_given:
        random_cards = generate_cards()
        cards_given = True

    for i, card in enumerate(random_cards):
        image = pygame.image.load(f'playing_cards_pictures/{card}')
        screen.blit(image, (x + i * 80, y))

    for i in range(4):
        image = pygame.image.load(f'playing_cards_pictures/back.png')
        screen.blit(image, (x2, y2 + 80 * i))

    for i in range(4):
        image = pygame.image.load(f'playing_cards_pictures/back.png')
        screen.blit(image, (x3, y2 + 80 * i))

    pygame.display.flip()

pygame.quit()
