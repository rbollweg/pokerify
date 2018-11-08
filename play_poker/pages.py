from otree.api import Currency as c, currency_range
from otree.api import widgets
from pandas import json
from ._builtin import Page, WaitPage
from .models import Constants
from django.forms import modelformset_factory
import random
import ast
from play_poker.backend_stats import odds_of_winning
from play_poker.poker_controller import PokerGame, Round, get_hand_type, determine_hand_winner
from django import forms


def convert_hand_type_to_text(hand_type):
    if hand_type == 0:
        return 'Card High'
    if hand_type == 1:
        return 'Pair'
    if hand_type == 2:
        return 'Two Pair'
    if hand_type == 3:
        return 'Three of a Kind'
    if hand_type == 4:
        return 'Straight'
    if hand_type == 5:
        return 'Flush'
    if hand_type == 6:
        return 'Full House'
    if hand_type == 7:
        return 'Four of a Kind'
    if hand_type == 8:
        return 'Straight Flush'
    if hand_type == 9:
        return 'Royal Flush'


class PokerPage(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        odds = odds_of_winning(self.player.get_hand())
        hand_type = convert_hand_type_to_text(get_hand_type(self.player.get_hand()))
        if odds == 0:  # Statistics for card high needs to be updated, this is an approximation for high card winning for Ace high
            odds = 7.736
        return {'hand': self.player.convert_to_text(self.player.get_hand()), 'odds': odds, 'hand_type': hand_type}


class PokerWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.session.vars['is_deck_created'] = False
        self.session.vars['current_round'].winners = determine_hand_winner(
            self.session.vars['current_round'].player_hands)
        if len(self.session.vars['current_round'].winners) > 1:
            self.session.vars['current_round'].is_tie = True


class ResultsPage(Page):
    def before_next_page(self):
        self.session.vars['game'].rounds.append(self.session.vars['current_round'])  # Log current round
        print('Shuffling Deck')
        self.session.vars['game'].deck = PokerGame.create_deck()  # shuffle the deck after each round
        print('Starting Next Round')
        self.session.vars['current_round'] = Round(self.session.vars['game'].deck,
                                                   Constants.players_per_group)  # Start the next round

    def vars_for_template(self):
        winner = False
        print('Winners: ' + str(self.session.vars['current_round'].winners))
        if (self.participant.id_in_session - 1) in self.session.vars['current_round'].winners:
            print('Player ' + str(self.participant.id_in_session) + ' wins this round')
            winner = True
        hand_type = convert_hand_type_to_text(self.player.get_hand())
        return {'winner': winner, 'tie': self.session.vars['current_round'].is_tie, 'hand_type': hand_type}


page_sequence = [PokerPage, PokerWaitPage, ResultsPage]
