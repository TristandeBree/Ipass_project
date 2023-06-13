import pygame
import random
from Card import Card
from Player import Player
import game_items

# initiating pygame
pygame.init()

# making the screen
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode([1400,1200])

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


player1 = Player(0, True, generate_cards())
player2 = Player(1, False, generate_cards())
player3 = Player(2, False, generate_cards())

player1.set_neighbours(player2, player3)

handled = []

while running:
    y = 600
    x2 = 100
    y2 = 100
    x3 = 1400

    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill((0, 0, 0))

    if not cards_given:
        random_cards = generate_cards()
        cards_given = True

    for i, card in enumerate(random_cards):
        image = pygame.image.load(f'playing_cards_pictures/{card}.png')
        x = 600 + i * 80
        screen.blit(image, (x, y))
        if image.get_rect(center=(x + image.get_width() / 2, y + image.get_height() / 2)).collidepoint(pos):
            pygame.draw.rect(screen, (255,255,0), pygame.Rect(x, y, image.get_width(), image.get_height()), 2)
            if pygame.mouse.get_pressed()[0] and card not in handled:
                handled.append(card)
                print(card)

    for i in range(4):
        image = pygame.image.load(f'playing_cards_pictures/back.png')
        screen.blit(image, (x2, y2 + 80 * i))

    for i in range(4):
        image = pygame.image.load(f'playing_cards_pictures/back.png')
        screen.blit(image, (x3, y2 + 80 * i))

    pygame.display.flip()

pygame.quit()
