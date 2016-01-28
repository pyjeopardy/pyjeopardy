from copy import deepcopy
from importlib import import_module

from pyjeopardy import config

from .hardware import Keyboard
from .log import Log

class Game:
    def __init__(self):
        self.rounds = []
        self.players = []
        self.hardware = []
        self.log = None

        # add keyboard as hardware
        self.keyboard = Keyboard()
        self.hardware.append(self.keyboard)

        # add hardware given in config
        for mod_name,class_name in config.HARDWARE:
            mod = import_module(mod_name)
            hw = getattr(mod, class_name)

            self.hardware.append(hw())

        self.free_colors = deepcopy(config.COLORS)

    def reset_log(self):
        self.log = Log()

    def add_round(self, round):
        self.rounds.append(round)

    def add_player(self, player):
        self.free_colors.remove(player.color)

        self.players.append(player)

    def is_active_hardware(self):
        for hw in self.hardware:
            if hw.active:
                return True
        return False

    def used_keys_for_hardware(self, hardware):
        if hardware not in self.hardware:
            return None

        keys = []
        for player in self.players:
            if player.hardware == hardware:
                keys.append(player.key)

        return keys
