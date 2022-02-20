from PyQt5 import QtWidgets
import sys
import pygame
from pygame import color
from ColoringAlgos import ColoringAlgos
from graph import *
from view.MainWindow import MainWindow

from consts import *

import matplotlib.pyplot as plt
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

def run_map():
    import usages.world_map.world_map as wm

    wm.load_us()
    wm.load_fr()
    
def run_schedule():
    import usages.schedule.schedule as sch

    sch.main_schedule()

if __name__ == "__main__":
    run_schedule()
    # start_gui()