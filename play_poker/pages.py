from otree.api import Currency as c, currency_range
from otree.api import widgets
from pandas import json
from ._builtin import Page, WaitPage
from .models import Constants
from django.forms import modelformset_factory
import random
import ast
from play_poker.poker_controller import PokerGame
from django import forms


class PokerPage(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        if not self.session.vars['set_up']:
            game = PokerGame()
            game.set_up()
            self.session.vars['game'] = game
            self.session.vars['set_up'] = True
        return {'hand': self.player.get_hand()}


class ResultsPage(WaitPage):

    def after_all_players_arrive(self):
        a = 1
        # determine winner


page_sequence = [PokerPage]
