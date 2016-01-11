from PySide.QtGui import QColor

COLORS=[
    ('red', QColor(255, 0, 0)),
    ('green', QColor(0, 255, 0)),
    ('blue', QColor(0, 0, 255)),
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
