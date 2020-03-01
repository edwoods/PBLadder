from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from FileIo import LoadPreferences
from PBLadder import Ui_MainWindow

if __name__ == "__main__":
    LoadPreferences()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle("Pickleball Schedule Maker")
    MainWindow.show()


    sys.exit(app.exec_())
