import pygame

class Helper:
    def baby_mode(self, player, card_played, screen):
        best_cards = []
        for card in player.hand:
            if card_played is not None and card.suit == card_played.suit:
                best_cards.append(card)

        if not best_cards:
            card_to_recommend = min(player.hand)
        else:
            card_to_recommend = best_cards[0]
            for card in best_cards:
                if card > card_to_recommend:
                    card_to_recommend = card

        for i, card in enumerate(player.hand):
            if card == card_to_recommend:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(600 + i * 80, 600, 75, 109), 3)
