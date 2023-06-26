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

# making the screen
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode([1400,1200])

running = True

font = pygame.font.Font('freesansbold.ttf', 20)
menu = Menu()
helper = Helper()

pick_players = False
pick_ai = False

amount_of_players = 0
ai_type = ''

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill((0, 0, 0))

    if pick_players and pick_ai:
        text = font.render(f'Current player: {current_player}', False, (0, 255, 0))
        screen.blit(text, (500, 200))

        playing_table.draw_hand(current_player, screen)

        playing_table.draw_rond(screen)

        match ai_type:
            case 'baby':
                helper.baby_mode(current_player, playing_table, screen)
            case 'better':
                helper.better_mode(current_player, playing_table, screen)
            case 'MCCFR':
                helper.begin_MCCFR(current_player, playing_table, screen)

        playing_table.draw_played_cards(screen)

        playing_table.draw_scores(screen)

        current_player = playing_table.play_action(screen, current_player)
    else:

        if not pick_players:
            text = font.render("Choose the amount of players to play with: ", False, (255, 255, 255))
            screen.blit(text, (150, 550))
            amount_of_players = menu.get_player_amount(screen, font)
        else:
            text = font.render(f'Amount of players: {amount_of_players}', False, (255, 255, 255))
            screen.blit(text, (150, 550))

        if not pick_ai:
            text = font.render("Choose the AI you want to play with: ", False, (255, 255, 255))
            screen.blit(text, (850, 600))
            ai_type = menu.get_ai_type(screen, font)
        else:
            text = font.render(f'The ai of your choice: {ai_type}', False, (255, 255, 255))
            screen.blit(text, (850, 600))

        if type(amount_of_players) == int and amount_of_players > 0:
            pick_players = True
            if pick_ai:
                playing_table = Table(amount_of_players)
                current_player = playing_table.find_starting_player()

        if ai_type != '':
            pick_ai = True
            if pick_players:
                playing_table = Table(amount_of_players)
                current_player = playing_table.find_starting_player()

    pygame.display.flip()

pygame.quit()
