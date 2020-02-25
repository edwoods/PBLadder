import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMessageBox


def loadCsv(MainWindow):
    path = QtCore.QDir.homePath()
    path2 = QtCore.QDir.currentPath()

    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open CSV", path2, "CSV (*.csv *.tsv)")

    # make sure that you don't already have this file open
    name = QFileInfo(fileName).fileName()
    #: :type: Ui_MainWindow
    if MainWindow.IsFileOpen(name):
        msg = QMessageBox.warning(None, "File is already open",
                                  "The file: '" + name + "' is already open")
        return

    list = []
    with open(fileName, "r") as fileInput:
        for row in csv.reader(fileInput):
            list.append(row)

    MainWindow.MakeNewTab(name, list)


def SaveAsCsv(fileName, table):
    # table = QtWidgets.QTableWidget()

    with open('v1 ' + fileName, 'w',newline='') as file:
        writer = csv.writer(file)

        line = []
        for col in range(table.columnCount()):
            line.append(table.horizontalHeaderItem(col).text())

        writer.writerow(line)

        for row in range(table.rowCount()):
            line = []
            for col in range(table.columnCount()):
                line.append(table.item(row, col).text())
            writer.writerow(line)



