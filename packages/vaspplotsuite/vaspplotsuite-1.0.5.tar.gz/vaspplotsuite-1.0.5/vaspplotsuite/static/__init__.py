from PyQt6.QtGui import QFontDatabase, QGuiApplication
from os import path

a = QGuiApplication([])
font_path = path.dirname(__file__)
font = QFontDatabase.addApplicationFont(font_path + "/Montserrat-Regular.ttf")
font = QFontDatabase.applicationFontFamilies(font)
