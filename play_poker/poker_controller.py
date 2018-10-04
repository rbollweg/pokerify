# Python program to shuffle a deck of card using the module random and draw 5 cards

# import modules
import itertools, random

from .models import Constants


class PokerGame:

    player_scores = []
    deck = []
    player_hands = []

    def set_up(self):
        self.deck = self.create_deck(self)
        self.player_hands = self.deal_hands(self, self.deck, Constants.players_per_group)

    @staticmethod
    def create_deck(self):
        # make a deck of cards
        deck = list(itertools.product(range(1, 14), ['Spades', 'Hearts', 'Diamonds', 'Clubs']))
        # shuffle the cards
        random.shuffle(deck)

        for index, card in enumerate(deck):
            deck[index] = Card(card[0], card[1])  # replace with our card object

        return deck

    @staticmethod
    def deal_hands(self, deck, num_players):
        # draw five cards
        player_hands = []
        for pl in range(num_players):
            hand = []
            for i in range((pl * 5) -5, (pl * 5)):
                print("Dealt " + str(deck[i].value) + " of " + deck[i].suit + "- Player " + str(pl))
                hand.append(deck[i])
            player_hands.append(hand)
        return player_hands


class Card:
    def __init__(self, value, suit):
        if value > 10:
            if value == 11:
                value = 'Jack'
            if value == 12:
                value = 'Queen'
            if value == 13:
                value = 'King'
            if value == 14:
                value = 'Ace'
        self.value = value
        self.suit = suit

