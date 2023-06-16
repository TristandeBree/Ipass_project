import pygame
from Player import Player
import time
import game_items


class Table:
    def __init__(self, amount_of_players):
        self.card_deck = game_items.generate_cards()
        self.players = self.generate_players(amount_of_players)
        self.set_players()
        self.scores = self.set_scores()
        self.main_card = None
        self.font = pygame.font.Font('freesansbold.ttf', 24)


    def generate_players(self, amount_of_players):
        players = []
        for i in range(amount_of_players):
            if i == 0:
                players.append(Player(i + 1, True, game_items.generate_4_cards(self.card_deck)))
                self.remove_from_deck(players[i].hand)
            else:
                players.append(Player(i + 1, False, game_items.generate_4_cards(self.card_deck)))
                self.remove_from_deck(players[i].hand)
        return players

    def set_players(self):
        for i in range(len(self.players)):
            if len(self.players) - 1 != i:
                self.players[i].left = self.players[i + 1]
                self.players[i].right = self.players[i - 1]
            else:
                self.players[i].left = self.players[0]
                self.players[i].right = self.players[i - 1]
            if i == 0:
                self.players[i].right.last = True

    def remove_from_deck(self, cards_to_remove):
        for card in cards_to_remove:
            self.card_deck.remove(card)

    def reset_card_deck(self):
        self.card_deck = game_items.generate_cards()

    def set_scores(self):
        return [0 for i in range(len(self.players))]

    def draw_scores(self, screen):
        for i, score in enumerate(self.scores):
            score = self.font.render(str(score), False, (255, 255, 255))
            screen.blit(score, (900 + 25 * i, 450))
            player_number = self.font.render(str(i + 1), False, (255, 255, 255))
            screen.blit(player_number, (900 + 25 * i, 425))

    def draw_played_cards(self, screen):
        for i, player in enumerate(self.players):
            if player.played is not None:
                image = pygame.image.load(f'playing_cards_pictures/{player.played}.png')
                screen.blit(image, (500 + i * 75, 300))
            else:
                pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(500 + i * 75, 300, 75, 109), 2)
            text = self.font.render(str(player.number), False, (255, 255, 255))
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
                    print("Player that was winning: " + str(winning))
                    print("winning variable before: " + str(winning.won))
                    winning.won = False
                    print("winning variable after: " + str(winning.won))
                    winning = player
                    print("new winning player:" + str(winning))
                    winning.won = True
                player.played = None

        if round_number == 4:
            self.reset_card_deck()
            for player in self.players:
                if not player.won:
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
