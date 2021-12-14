from PyQt5 import QtWidgets
import sys
import pygame
from pygame import color
from ColoringAlgos import ColoringAlgos
from graph import EdgesSet
from view.MainWindow import MainWindow

from consts import *

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
    start_gui()