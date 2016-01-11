from copy import deepcopy

from pyjeopardy import config

class Game:
    def __init__(self):
        self.rounds = []
        self.players = []

        self.free_colors = deepcopy(config.COLORS)

    def add_round(self, round):
        self.rounds.append(round)

    def add_player(self, player):
        # a bit ugly…
        color_name = config.get_color_name(player.color)
        self.free_colors.remove((color_name, player.color))

        self.players.append(player)
