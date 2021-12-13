from PyQt5 import QtWidgets
import sys
import pygame
from view.MainWindow import MainWindow

from consts import *

if __name__ == "__main__":
    pygame.init()
    my_surface=pygame.Surface((WIDTH, HEIGHT))
    my_surface.fill((200,0,0))
    
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    my_window=MainWindow(my_surface)
    my_window.show()
    app.exec_()