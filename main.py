from PyQt5 import QtWidgets
import sys
import pygame
from pygame import color
from ColoringAlgos import ColoringAlgos
from graph import *
from view.MainWindow import MainWindow

from consts import *

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.subplots as ps
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.io as pio

def start_gui():
    pygame.init()
    my_surface=pygame.Surface((WIDTH, HEIGHT))
    my_surface.fill((200,0,0))
    
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    my_window=MainWindow(my_surface)
    my_window.show()
    app.exec_()

if __name__ == "__main__":
    # start_gui()

    import usages.world_map as wm
    df, geo = wm.load_fr()

    fig = px.choropleth_mapbox(df, geojson=geo, color="color",
                            locations="stusab", featureidkey="properties.code",
                            center={"lat": 42.5517, "lon": -97.7073},
                            mapbox_style="carto-positron", zoom=4, color_discrete_sequence=COLORS_ORDER)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_image("fig1.png")
    fig.show()
        