import pygame
import math
import time


class Menu:
    def get_player_amount(self, screen, font):
        """
        a part of the menu which draws boxes with numbers in it for the player to pick with how many players you want to play
        :param screen: the screen on which needs to be drawn
        :param font: the font of the text
        :return: the amount of players that is selected
        """
        for i in range(1,8):
            rect = pygame.Rect(400 + i % 4 * 50, 600 + math.floor(i / 4) * 50, 50, 50)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            text = font.render(str(i + 1), False, (255, 255, 255))
            screen.blit(text, (415 + i % 4 * 50, (600 + 15) + math.floor(i / 4) * 50))
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                amount_of_players = i + 1
                time.sleep(0.2)
                return amount_of_players

    def get_ai_type(self, screen, font):
        """
        a part of the menu that draws the options for the AI that can be used to give recommendations
        :param screen: the screen that needs to be drawn on
        :param font: the font of the text
        :return: the type of AI that the player wants
        """
        types = ['baby', 'better', 'MCCFR']
        for i in range(len(types)):
            rect = pygame.Rect(850, 650 + i * 50, 150, 50)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            text = font.render(types[i], False, (255, 255, 255))
            screen.blit(text, (865, 665 + i * 50))
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                time.sleep(0.2)
                return types[i]
        return ''
