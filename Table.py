import pygame
from Player import Player
import time
import game_items


class Table:
    def __init__(self, amount_of_players):
        """
        initialize the table
        :param amount_of_players: the amount of players that are playing this game
        """
        self.card_deck = game_items.generate_cards()
        self.players = self.generate_players(amount_of_players)
        self.set_players()
        self.scores = self.set_scores()
        self.main_card = None
        self.last_won = None
        self.last_won_card = None
        self.round = 1
        self.font = pygame.font.Font('freesansbold.ttf', 24)

    def is_winning(self, card):
        """
        checks if the card given is better than the first card played
        :param card: the card that is played
        :return: True if the card is better and false if it is worse
        """
        winning_player = self.find_starting_player()
        if winning_player.played is None or card > winning_player.played and card.suit == winning_player.played.suit:
            return True
        else:
            return False

    def generate_players(self, amount_of_players):
        """
        generates the players and gives them 4 random cards
        :param amount_of_players: the amount of players that need to be generated
        :return: a list of players with random cards and a unique number
        """
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
        """
        Sets the players neighbours, so we know who is next.
        :return: None
        """
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
        """
        removes cards from the main deck
        :param cards_to_remove: the list of cards that need to be removed
        :return: None
        """
        for card in cards_to_remove:
            self.card_deck.remove(card)

    def reset_card_deck(self):
        """
        regenerates the card deck
        :return: None
        """
        self.card_deck = game_items.generate_cards()

    def set_scores(self):
        """
        sets the scores for the players
        :return: a list of 0's for all of the players
        """
        return [0 for i in range(len(self.players))]

    def draw_scores(self, screen):
        """
        draws the scores of the players on the screen
        :param screen: the screen that needs to be drawn on
        :return: None
        """
        for i, score in enumerate(self.scores):
            score = self.font.render(str(score), False, (255, 255, 255))
            screen.blit(score, (900 + 25 * i, 450))
            player_number = self.font.render(str(i + 1), False, (255, 255, 255))
            screen.blit(player_number, (900 + 25 * i, 425))

    def draw_played_cards(self, screen):
        """
        Draws the cards that have been played by the players at the table
        :param screen: the screen that needs to be drawn on
        :return: None
        """
        for i, player in enumerate(self.players):
            if player.played is not None:
                image = pygame.image.load(f'playing_cards_pictures/{player.played}.png')
                screen.blit(image, (500 + i * 75, 300))
            else:
                pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(500 + i * 75, 300, 75, 109), 2)
            text = self.font.render(str(player.number), False, (255, 255, 255))
            screen.blit(text, (525 + i * 75, 275))

    def draw_rond(self, screen):
        """
        draws the round number that the players are at
        :param screen: the screen that needs to be drawn at
        :return: None
        """
        text = self.font.render(f'round: {self.round}', False, (255, 255, 255))
        screen.blit(text, (300, 300))

    def draw_hand(self, player, screen):
        """
        Draws the hand of the player
        :param player: the player which is doing something
        :param screen: the screen that needs to be drawn on
        :return: None
        """
        for i, card in enumerate(player.hand):
            image = pygame.image.load(f'playing_cards_pictures/{card}.png')
            x = 600 + i * 80
            y = 600
            screen.blit(image, (x, y))

    def find_starting_player(self):
        """
        finds the starting player
        :return: the player that moved first
        """
        for player in self.players:
            if player.first:
                return player

    def find_last_player(self):
        """
        finds the player that is last
        :return: the last player
        """
        for player in self.players:
            if player.last:
                return player

    def check_results(self):
        """
        checks all the cards that have been played in the round and checks if the cards played after the first one
        are better. If so a new winner is set, and they will be first next round. If it is the final round it will check
        for a winner and the rest of the table gets points.
        :return: None
        """
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

        self.last_won = winning
        self.last_won_card = winning_card_played

        if self.round == 4:
            self.reset_card_deck()
            self.round = 1
            for player in self.players:
                if not player.won:
                    self.scores[player.number - 1] += 1
                player.hand = game_items.generate_4_cards(self.card_deck)
                self.remove_from_deck(player.hand)
            winning.left.first = True
            winning.last = True
            print(self.scores)
            print(self.find_starting_player())
            return

        winning.first = True
        winning.right.last = True
        winning.won = False

    def play_action(self, screen, player):
        """
        calls the action of the player and checks if they are last or first, if they are last it will check the results
        after they have made their move, and if they are first it will set the main card of the table to that card.
        :param screen: the screen that needs to be drawn at
        :param player: the player that is currently making a move
        :return: The next player that has to move, except if no move has been made, then it will return the base player
        """
        if player.last:
            move_made = player.player_action(screen, self.main_card)
            if move_made:
                self.check_results()
                self.round += 1
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
