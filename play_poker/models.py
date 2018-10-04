from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
)
from otree.db.models import Model, ForeignKey


author = 'Ryan Bollweg'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Pokerify'
    players_per_group = 4
    num_rounds = 100


class Subsession(BaseSubsession):

    def creating_session(self):
        self.session.vars['game'] = {}
        self.session.vars['set_up'] = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    winner = models.BooleanField(initial=False)

    def get_hand(self):
        return self.session.vars['game'].player_hands[self.id_in_group-1]



