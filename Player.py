from Card import Card
import pygame
import time
class Player:
    def __init__(self, number, first, hand):
        self.number = number
        self.played = None
        self.first = first
        self.hand = hand
        self.left = None
        self.right = None
        self.last = False
        self.won = False

    def player_action(self, screen, card_played):
        action = False
        handled = []

        if card_played is not None:
            for card in self.hand:
                if card.suit != card_played.suit:
                    handled.append(card)
            if len(handled) == len(self.hand):
                handled = []

        for i, card in enumerate(self.hand):
            image = pygame.image.load(f'playing_cards_pictures/{card}.png')
            x = 600 + i * 80
            y = 600
            if image.get_rect(center=(x + image.get_width() / 2, y + image.get_height() / 2)).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x, y, image.get_width(), image.get_height()), 2)
                if pygame.mouse.get_pressed()[0] and card not in handled:
                    handled.append(card)
                    self.hand.remove(card)
                    time.sleep(0.35)
                    self.played = card
                    action = True
        if action:
            return True
        else:
            return False

    def __str__(self):
        # return f'Player: {self.number} played: {self.played.number} of {self.played.suit}'
        return f'Player {self.number}'

    def __eq__(self, other):
        return self.number == other.number

