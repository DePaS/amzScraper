from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(660, 390, 600, 300)
    win.setWindowTitle("Amazon scraper")

    win.show()
    sys.exit(app.exec_())

window()
