import pygame
import math
from Menu import Menu
from Helper import Helper
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

running = True

font = pygame.font.Font('freesansbold.ttf', 32)
menu = Menu()
helper = Helper()

pick_players = False

amount_of_players = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill((0, 0, 0))

    if pick_players:
        text = font.render(f'Current player: {current_player}', False, (0, 255, 0))
        screen.blit(text, (500, 200))

        playing_table.draw_hand(current_player, screen)

        helper.baby_mode(current_player, playing_table.main_card, screen)

        playing_table.draw_played_cards(screen)

        playing_table.draw_scores(screen)

        current_player = playing_table.play_action(screen, current_player)
    else:
        text = font.render("Choose the amount of players to play with: ", False, (255, 255, 255))
        screen.blit(text, (350, 250))

        amount_of_players = menu.get_player_amount(screen, font)

        if type(amount_of_players) == int and amount_of_players > 0:
            playing_table = Table(amount_of_players)
            current_player = playing_table.find_starting_player()
            pick_players = True

    pygame.display.flip()

pygame.quit()
