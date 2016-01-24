class Player:
    def __init__(self, name, color, hardware, key):
        self.name = name
        self.points = 0
        self.color = color

        self.hardware = hardware
        self.key = key

    def add_points(self, points):
        self.points += points
