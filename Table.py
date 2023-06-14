import pygame
import time
import game_items


class Table:
    def __init__(self):
        self.players = []
        self.scores = []
        self.main_card = None
        self.card_deck = game_items.generate_cards()

    def remove_from_deck(self, cards_to_remove):
        for card in cards_to_remove:
            self.card_deck.remove(card)

    def reset_card_deck(self):
        self.card_deck = game_items.generate_cards()

    def set_scores(self):
        self.scores = [0 for i in range(len(self.players))]

    def draw_played_cards(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 24)
        for i, player in enumerate(self.players):
            if player.played is not None:
                image = pygame.image.load(f'playing_cards_pictures/{player.played}.png')
                screen.blit(image, (500 + i * 75, 300))
            text = font.render(str(player.number), False, (255, 255, 255))
            screen.blit(text, (525 + i * 75, 275))

    def draw_hand(self, player, screen):
        for i, card in enumerate(player.hand):
            image = pygame.image.load(f'playing_cards_pictures/{card}.png')
            x = 600 + i * 80
            y = 600
            screen.blit(image, (x, y))

    def find_starting_player(self):
        for player in self.players:
            if player.first:
                return player

    def find_last_player(self):
        for player in self.players:
            if player.last:
                return player

    def check_results(self, round_number):
        first = self.find_starting_player()
        first.right.last = False
        first.first = False
        first.played = None
        winning_card_played = self.main_card
        suit = self.main_card.suit
        winning = first
        winning.won = True
        for player in self.players:
            if player != first:
                if player.played.suit == suit and player.played > winning_card_played:
                    winning_card_played = player.played
                    winning.won = False
                    winning = player
                    winning.won = True
                player.played = None

        if round_number == 4:
            self.reset_card_deck()
            for player in self.players:
                if not player.won:
                    print(player)
                    self.scores[player.number - 1] += 1
                player.hand = game_items.generate_4_cards(self.card_deck)
                self.remove_from_deck(player.hand)
            first.left.first = True
            first.last = True
            print(self.scores)
            print(self.find_starting_player())
            return

        winning.first = True
        winning.right.last = True
        winning.won = False

    def play_action(self, screen, player):
        if player.last:
            move_made = player.player_action(screen, self.main_card)
            if move_made:
                self.check_results(4 - len(player.hand))
                return self.find_starting_player()
        elif player.first:
            move_made = player.player_action(screen, None)
            self.main_card = player.played
            if move_made:
                return player.left
        else:
            move_made = player.player_action(screen, self.main_card)
            if move_made:
                return player.left
        return player
