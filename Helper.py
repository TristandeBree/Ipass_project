import pygame

class Helper:
    def baby_mode(self, player, table, screen):
        """
        baby_mode Helping algorithm basicly follows the rules, if it needs to follow suit
        it will, and it will play the lowest card in order to keep the high ones for the later rounds.
        Else it will play the lowest card in your hand
        :param table: the table at which the round is played
        :param player: the player that needs the recommendation
        :param screen: the screen the recommendations needs to be drawn on
        :return: None
        """
        best_cards = []
        for card in player.hand:
            if table.main_card is not None and card.suit == table.main_card.suit:
                best_cards.append(card)

        if not best_cards:
            card_to_recommend = min(player.hand)
        else:
            card_to_recommend = best_cards[0]
            for card in best_cards:
                if card < card_to_recommend:
                    card_to_recommend = card

        for i, card in enumerate(player.hand):
            if card == card_to_recommend:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(600 + i * 80, 600, 75, 109), 3)

    def better_mode(self, player, table, screen):
        """
        A better version of the baby version, this version will try to combo cards. Which means
        that you will play 2 cards of the same suit after eachother when you won.
        :param player: the player that needs recommendatinos
        :param table: the table at which the game is played
        :param screen: the screen on which needs to be drawn
        :return: None
        """
        best_cards = []
        for card in player.hand:
            if table.main_card is not None and card.suit == table.main_card.suit:
                best_cards.append(card)
            elif table.last_won is not None and table.last_won == player and table.last_won_card.suit == card.suit:
                best_cards.append(card)
            elif table.find_starting_player() == player:
                suits = player.check_suits_in_hand()
                for suit, amount in suits.items():
                    if amount > 1:
                        for new_card in player.hand:
                            if new_card.suit == suit:
                                best_cards.append(new_card)
                break

        if not best_cards:
            card_to_recommend = min(player.hand)
        else:
            card_to_recommend = best_cards[0]
            for card in best_cards:
                if table.is_winning(card) and len(best_cards) > 1:
                    card_to_recommend = max(best_cards)
                elif table.last_won is not None and table.last_won == player and card.suit == table.last_won_card.suit \
                        and table.round - 1 + len(best_cards) == 4:
                    card_to_recommend = card
                else:
                    card_to_recommend = min(best_cards)

        # draw a little edge around the card that needs to be recommended
        for i, card in enumerate(player.hand):
            if card == card_to_recommend:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(600 + i * 80, 600, 75, 109), 3)

    def begin_MCCFR(self, player, table, screen):
        """
        The base for the MCCFR algorithm, which will according to the game tree created by the cards in your hand
        pick what option is the best to play and will recommend that card.
        :param player: the player that is playing
        :param table: the table at which the game is being played
        :param screen: the screen on which needs to be drawn
        :return: None
        """

        def calculate_card_value(card):
            """
            gives a card value
            :param card: the card that needs to be evaluated
            :return: the value of that card according to the dictionary
            """
            value_dict = {'jack': -4, 'queen': -3, 'king': -2, 'ace': -1, '7': 1, '8': 2, '9': 3, '10': 4}
            return value_dict[card.number]

        def optimal_path(cards, reach_prob, card_sequence, accumulated_regret, base=1, other_player_card=None):
            """
            This is the main loop of the algorithm, here we calculate the value of each card and try to find the best
            one. If the best one is found, we remove it from the cards as if it is being played and check the rest of the
            game tree.
            :param cards: the cards that need to be ranked
            :param reach_prob: the probability this card combination will be reached
            :param card_sequence: the cards that have been played up untill now
            :param accumulated_regret: the regret per card
            :param base: the base reach probability
            :param other_player_card: the card which suit needs to be followed
            :return: the card sequence that is most optimal to play
            """
            num_cards = len(cards)

            if num_cards == 0:
                cards_to_play = card_sequence
                return cards_to_play

            if other_player_card is not None:
                desired_suit = other_player_card.suit
            else:
                desired_suit = None

            #give the cards that are a legal move
            filtered_cards = [card for card in cards if card.suit == desired_suit] if desired_suit else cards

            expected_values = [calculate_card_value(card) for card in filtered_cards]
            counterfactual_value = sum([reach * value for reach, value in zip(reach_prob, expected_values)])
            instantanious_regret = [reach * value - counterfactual_value for reach, value in zip(reach_prob, expected_values)]
            accumulated_regret = [regret + reach * value for regret, reach, value in zip(accumulated_regret, reach_prob, expected_values)]

            if not filtered_cards:
                card_to_play = min(cards)
                card_index = cards.index(card_to_play)
                new_card_sequence = card_sequence + [card_to_play]
                new_cards = cards[:card_index] + cards[card_index + 1:]
                return optimal_path(new_cards, [reach_prob[0]/base], new_card_sequence, accumulated_regret, base + 1, other_player_card)
            else:
                card_index = max(range(len(filtered_cards)), key=expected_values.__getitem__)
                card_to_play = filtered_cards[card_index]

                new_card_sequence = card_sequence + [card_to_play]
                new_cards = cards[:card_index] + cards[card_index + 1:]
                return optimal_path(new_cards, [reach_prob[0] / base], new_card_sequence, accumulated_regret, base + 1, other_player_card)

        # find the best card to play with the hand of the player
        card_to_play = optimal_path(player.hand, [1], [], [0] * len(player.hand), other_player_card=table.main_card)[0]

        # draw a little edge around the card which is recommended
        for i, card in enumerate(player.hand):
            if card == card_to_play:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(600 + i * 80, 600, 75, 109), 3)