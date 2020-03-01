import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os, re

prefs = {}


def LoadPreferences():

    prefs['startPath'] = os.path.normpath(os.getcwd())
    prefs['nWeeks'] = 10
    prefs['scoreScale'] = 4
    prefs['dir'] = os.path.normpath(os.getcwd())

    with open('preferences.txt', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        f.close()

        # parse the data
        for line in data:
            if not line:
                pass
            elif len(line) == 2:
                prefs[line[0]] = line[1].strip()

            elif line[2].strip() == 'int':
                prefs[line[0]] = int(line[1].strip())

            elif line[2].strip() == 'float':
                prefs[line[0]] = float(line[1].strip())

    try:
        os.chdir(prefs['dir'])
    except:
        print("os.chdir failed: " + prefs['dir'])

    prefs['sessions'] = ['w' + str(n+1) for n in range(prefs['nWeeks'])]
    prefs['byeScore'] = -1.1 * prefs['scoreScale']

    return


def loadCsv(MainWindow):
    path = os.path.normpath(os.getcwd())
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open CSV", path, "CSV (*.csv *.tsv)")
    if not fileName:
        return
    # make sure that you don't already have this file open
    pathAndName = os.path.split(fileName)

    name = pathAndName[1]
    filePath = os.path.normpath(pathAndName[0])

    # save the path name in the prefs file if it changes
    curPath = os.path.normpath(os.getcwd())
    if filePath != curPath:
        os.chdir(prefs['startPath'])
        with open('preferences.txt', 'a') as f:
            f.writelines(['\n', 'dir,' + filePath])
        f.close()
        os.chdir(filePath)   # cd to the selected path

    #: :type: Ui_MainWindow
    if MainWindow.IsFileOpen(name):
        QMessageBox.warning(None, "File is already open",
                                  "The file: '" + name + "' is already open")
        return

    list1 = []
    with open(fileName, "r") as fileInput:
        for row in csv.reader(fileInput):
            list1.append(row)

    MainWindow.MakeNewTab(name, list1)


def SaveAsCsv(fileName, table):
    # table = QtWidgets.QTableWidget()
    # do not over write the input file
    files = os.listdir(os.getcwd())
    if fileName in files:    # need to rename the file
        baseName = re.search(r"\w* w\d+", fileName, re.IGNORECASE).group()

        # create a new name for the file
        version = 1
        newName = ''
        while True:
            newName = baseName + '.v' + str(version) + '.csv'
            if newName in files:
                version += 1
            else:
                os.rename(fileName, newName)
                break


    with open(fileName, 'w', newline='') as file:
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
