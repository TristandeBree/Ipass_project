from Card import Card
import pygame
import time
class Player:
    def __init__(self, number, first, hand):
        """
        initialize the player
        :param number: the number of the player
        :param first: if the player is first or not
        :param hand: the hand of the player
        """
        self.number = number
        self.played = None
        self.first = first
        self.hand = hand
        self.left = None
        self.right = None
        self.last = False
        self.won = False

    def player_action(self, screen, card_played):
        """
        this function will check what cards the player has and if it is hovering over one of them. If so it will draw
        an edge around the card indicating that you are hovering over it. If you click it, it will update the player and
        send back that the player has made a move.
        :param screen: the screen that needs to be drawn on
        :param card_played: the card that is played, this is used for if the player has to follow suit
        :return: Boolean of if the player has done something or not
        """
        action = False
        handled = []

        # if a card has been played before the player's turn check his hand if it has cards of the same suit
        # if so, add the rest to a list so they can't be played anymore
        if card_played is not None:
            for card in self.hand:
                if card.suit != card_played.suit:
                    handled.append(card)
            if len(handled) == len(self.hand):
                handled = []

        for i, card in enumerate(self.hand):
            # load the cards but don't draw them
            image = pygame.image.load(f'playing_cards_pictures/{card}.png')
            x = 600 + i * 80
            y = 600
            # check if the card has the cursor on it
            if image.get_rect(center=(x + image.get_width() / 2, y + image.get_height() / 2)).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x, y, image.get_width(), image.get_height()), 2)
                # if the mouse has been pressed down and the card is not in the list of cards that can't be played
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

    def check_suits_in_hand(self):
        """
        checks the hand of the player and counts the amount of suits present
        :return: a frequency dictionary of every suit present
        """
        dict = {}
        for card in self.hand:
            if card.suit in dict.keys():
                dict[card.suit] += 1
            else:
                dict[card.suit] = 1
        return dict

    def __str__(self):
        # return f'Player: {self.number} played: {self.played.number} of {self.played.suit}'
        return f'Player {self.number}'

    def __eq__(self, other):
        return self.number == other.number

