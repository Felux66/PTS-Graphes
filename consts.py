from matplotlib import colors as mcolors
from random import shuffle

WIDTH, HEIGHT = 1000, 600

COLORS = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
# print(COLORS)

COLORS_ORDER = [
    "midnightblue", 
    "orchid", 
    "indianred", 
    "lightseagreen", 
    "royalblue", 
    "darkolivegreen", 
    "purple", 
    "orange", 
    "goldenrod", 
    "moccasin", 
    "sandybrown", 
    "mediumaquamarine",
    "dodgerblue",
    "deeppink",
    "gold",
    "peachpuff",
    "rebeccapurple",
    "thistle",
    "whitesmoke",
    "navy",
    "darkturquoise",
    "cornsilk",
    "mediumslateblue",
    "navajowhite",
    "tomato",
    "cornflowerblue",
    "chartreuse",
    "darkcyan",
    "seashell",
    "wheat",
    "yellowgreen",
]
shuffle(COLORS_ORDER)

NONE_COLOR = 'darkslategray'

DEFAULT_POINTS_DISTANCE = 70
DEFAULT_POINTS_DISTANCE_RANDOMNESS = 0.7
DEFAULT_POINTS_POSITIONING_ITERATIONS = 200
DEFAULT_POINTS_RADIUS = 25
DEFAULT_N_VERTICES_RANDGRAPH = 8
DEFAULT_DELETE_PROBABILITY = 0.7

DEFAULT_NEIGHBORS_INTERVAL = [1, DEFAULT_N_VERTICES_RANDGRAPH-1]