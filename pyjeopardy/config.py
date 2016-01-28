from pyjeopardy.game.color import Color

# available colors
COLORS=[
    Color("red",        255,    0,      0,      False),
    Color("lime",       0,      0,      255,    False),
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
    Color("navy",       0,      0,      128,    False),
]

# displayed number of players in one row during the game
NUM_PLAYERS_IN_ROW = 4

# font sizes
FONT_SIZE_ANSWER = 40
FONT_SIZE_ROUND_NAME = 25
FONT_SIZE_CATEGORIES = 20
FONT_SIZE_POINTS = 30
FONT_SIZE_LOG = 15

# list of available hardware
# format: (module path, class name)
HARDWARE = [('pyjeopardy.hardware.buzzer', 'Buzzer')]

# some helpful functions
#def get_color_for_name(name):
#    for col in COLORS:
#        if col[0] == name:
#            return col[1]
#    return None
#
#def get_color_name(color):
#    for col in COLORS:
#        if col[1] == color:
#            return col[0]
#    return None
