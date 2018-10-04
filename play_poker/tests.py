import random
from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Allocations, {'allocation_selection': random.randint(0, 3)})
        yield (pages.Results)
