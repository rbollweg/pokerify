from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
)
from copy import deepcopy
from play_poker.poker_controller import PokerGame, Round


author = 'Ryan Bollweg'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Pokerify'
    players_per_group = 2
    num_rounds = 100


class Subsession(BaseSubsession):

    def creating_session(self):
        if not self.session.config['set_up']:
            print('Executing Setup.')
            self.session.config['set_up'] = True
            self.session.vars['game'] = PokerGame()
            print('Creating Deck')
            self.session.vars['game'].deck = PokerGame.create_deck()
            print('Creating Round')
            self.session.vars['current_round'] = Round(self.session.vars['game'].deck, Constants.players_per_group)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    winner = models.BooleanField(initial=False)
    did_player_bet = models.BooleanField()

    def get_hand(self):
        return self.session.vars['current_round'].player_hands[self.id_in_group-1]

    def convert_to_text(self, hand):
        hand_copy = deepcopy(hand)
        for card in hand_copy:
            if card.value > 10:
                if card.value == 11:
                    card.value = 'Jack'
                if card.value == 12:
                    card.value = 'Queen'
                if card.value == 13:
                    card.value = 'King'
                if card.value == 14:
                    card.value = 'Ace'
        return hand_copy



