import os

from pyjeopardy.game.color import Color

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# available colors
COLORS=[
    Color("red",        255,    0,      0,      False),
    Color("blue",       0,      0,      255,    True),
    Color("yellow",     255,    255,    0,      False),
    Color("cyan",       0,      255,    255,    False),
    Color("magenta",    255,    0,      255,    False),
    Color("silver",     192,    192,    192,    False),
    Color("gray",       128,    128,    128,    False),
    Color("maroon",     128,    0,      0,      True),
    Color("olive",      128,    128,    0,      False),
    Color("green",      0,      128,    0,      False),
    Color("purple",     128,    0,      128,    True),
    Color("teal",       0,      128,    128,    False),
    Color("navy",       0,      0,      128,    True),
]

# displayed number of players in one row during the game
NUM_PLAYERS_IN_ROW = 4

# font sizes
FONT_SIZE_ANSWER = 40
FONT_SIZE_ROUND_NAME = 25
FONT_SIZE_CATEGORIES = 20
FONT_SIZE_POINTS = 30
FONT_SIZE_LOG = 15
FONT_SIZE_CUR_PLAYER = 30

# media files
MEDIA_DIR = os.path.join(BASE_DIR, 'pyjeopardy', 'media')
AUDIO_WAITING = os.path.join(MEDIA_DIR, 'jeopardy.wav')

# list of available hardware
# format: (module path, class name)
HARDWARE = [('pyjeopardy.hardware.buzzer', 'Buzzer')]
