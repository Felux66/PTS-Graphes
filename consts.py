from matplotlib import colors as mcolors

WIDTH, HEIGHT = 1000, 600

COLORS = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

COLORS_ORDER = ["indianred", "lightseagreen", "royalblue", "darkolivegreen", "purple", "orange", "goldenrod", "indigo", "moccasin", "sandybrown"]

NONE_COLOR = (50,50,50)

DEFAULT_POINTS_DISTANCE = 70
DEFAULT_POINTS_RADIUS = 25
DEFAULT_N_VERTICES_RANDGRAPH = 5

DEFAULT_NEIGHBORS_INTERVAL = [1, DEFAULT_N_VERTICES_RANDGRAPH-1]