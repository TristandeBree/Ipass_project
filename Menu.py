import pygame
import math
import time


class Menu:
    def get_player_amount(self, screen, font):
        for i in range(1,8):
            rect = pygame.Rect(400 + i % 4 * 50, 600 + math.floor(i / 4) * 50, 50, 50)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            text = font.render(str(i + 1), False, (255, 255, 255))
            screen.blit(text, (415 + i % 4 * 50, (600 + 15) + math.floor(i / 4) * 50))
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                amount_of_players = i + 1
                time.sleep(0.2)
                return amount_of_players
