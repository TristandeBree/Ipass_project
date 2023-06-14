import pygame
import random
from Card import Card
from Table import Table
from Player import Player
import game_items
import time

# initiating pygame
pygame.init()
pygame.event.pump()

# making the screen
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode([1400,1200])

cards = game_items.generate_cards()

running = True
cards_given = False

handled = []
cards_played = []

font = pygame.font.Font('freesansbold.ttf', 32)

playing_table = Table()

player1 = Player(1, True, game_items.generate_4_cards(playing_table.card_deck))
playing_table.remove_from_deck(player1.hand)
player2 = Player(2, False, game_items.generate_4_cards(playing_table.card_deck))
playing_table.remove_from_deck(player2.hand)
player3 = Player(3, False, game_items.generate_4_cards(playing_table.card_deck))
playing_table.remove_from_deck(player3.hand)

players = [player1, player2, player3]

player1.set_neighbours(player2, player3)
player2.set_neighbours(player3, player1)
player3.set_neighbours(player1, player2)

playing_table.players = players
playing_table.set_scores()

print(playing_table.scores)

current_player = playing_table.find_starting_player()

while running:
    y = 600
    x2 = 100
    y2 = 100
    x3 = 1400

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill((0, 0, 0))

    text = font.render(str(current_player), False, (0,255,0))
    screen.blit(text, (600, 200))

    playing_table.draw_hand(current_player, screen)

    playing_table.draw_played_cards(screen)

    current_player = playing_table.play_action(screen, current_player)

    for i in range(4):
        image = pygame.image.load(f'playing_cards_pictures/back.png')
        screen.blit(image, (x2, y2 + 80 * i))

    for i in range(4):
        image = pygame.image.load(f'playing_cards_pictures/back.png')
        screen.blit(image, (x3, y2 + 80 * i))

    pygame.display.flip()

pygame.quit()
