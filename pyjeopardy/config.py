from PySide.QtGui import QColor

COLORS=[
    ('red', QColor(255, 0, 0)),
    ('lime', QColor(0, 255, 0)),
    ('blue', QColor(0, 0, 255)),
    ('yellow', QColor(255,255,0)),
    ('cyan', QColor(0,255,255)),
    ('magenta', QColor(255,0,255)),
    ('silver', QColor(192,192,192)),
    ('gray', QColor(128,128,128)),
    ('maroon', QColor(128,0,0)),
    ('olive', QColor(128,128,0)),
    ('green', QColor(0,128,0)),
    ('purple', QColor(128,0,128)),
    ('teal', QColor(0,128,128)),
    ('navy', QColor(0,0,128))
]

def get_color_for_name(name):
    for col in COLORS:
        if col[0] == name:
            return col[1]
    return None

def get_color_name(color):
    for col in COLORS:
        if col[1] == color:
            return col[0]
    return None


NUM_PLAYERS_IN_ROW = 4

ANSWER_FONT_SIZE = 40
