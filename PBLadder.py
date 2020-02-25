# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PBLadder.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import re
from PyQt5.QtWidgets import QToolButton, QLabel, QTabBar, QTableWidget, QFrame, QMessageBox, QTableWidgetItem

from CopyAsHtml import CopyAsHtml
from FileIo import loadCsv, SaveAsCsv
from PlayerClass import PlayerType, AllPlayers, AllSubs, UpdateScores, ColHdrs


class Ui_MainWindow(object):
    # def __init__(self):

    def setupUi(self, MainWindow):
        AllPlayers['fileName'] = ''
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Pickleball Schedule Maker")
        MainWindow.resize(698, 629)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)

        self.verticalLayout.addWidget(self.tabWidget)

        # add a + button to add new tabs
        self.tb = QToolButton()
        self.tb.setText("+")
        self.lb = QLabel()
        self.tabWidget.addTab(self.lb, '')
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, self.tb)
        self.tb.clicked.connect(lambda:loadCsv(self))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 698, 21))

        self.menuFile = QtWidgets.QMenu('File', self.menubar)
        self.menuEdit = QtWidgets.QMenu('Edit', self.menubar)
        self.menuScheduling = QtWidgets.QMenu('Scheduling', self.menubar)

        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction('Open', MainWindow)
        self.actionSave = QtWidgets.QAction('Save', MainWindow)
        self.actionSave.setShortcut('Ctrl+S')

        self.actionPrint = QtWidgets.QAction('Print', MainWindow)
        self.actionQuit = QtWidgets.QAction('Quit', MainWindow)
        self.actionUpdate_with_current_scores = QtWidgets.QAction('Update with current scores', MainWindow)
        self.actionCopy_Current_Tab = QtWidgets.QAction('Copy Current Tab', MainWindow)
        self.actionCopy_Current_Tab.setShortcut('Ctrl+C')

        self.actionSchedule_Next_Matches = QtWidgets.QAction('Schedule Next Matches', MainWindow)
        self.actionSchedule_Next_Matches.setShortcut('Ctrl+N')

        self.actionAddSubs = QtWidgets.QAction('Add Subs', MainWindow)
        self.actionAddSubs.setShortcut('Alt+N')

        self.actionUpdateScoreSheet = QtWidgets.QAction('Update Score Sheet', MainWindow)
        self.actionUpdateScoreSheet.setShortcut('Ctrl+U')

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionQuit)

        self.menuEdit.addAction(self.actionCopy_Current_Tab)

        self.menuScheduling.addAction(self.actionSchedule_Next_Matches)
        self.menuScheduling.addAction(self.actionAddSubs)
        self.menuScheduling.addAction(self.actionUpdateScoreSheet)
        self.menuScheduling.addAction(self.actionUpdate_with_current_scores)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuScheduling.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pickleball Ladder Scheduler"))

        self.actionSave.triggered.connect(self.SaveFile)
        self.actionOpen.triggered.connect(self.OpenFile)
        self.actionAddSubs.triggered.connect(self.AddSubs)
        self.actionUpdateScoreSheet.triggered.connect(self.UpdateScoreSheet)

        self.actionCopy_Current_Tab.triggered.connect(self.CopyTable)

        self.actionSchedule_Next_Matches.triggered.connect(self.ScheduleNextMatches)
        self.actionUpdate_with_current_scores.triggered.connect(self.UpdateScores)
        self.tabWidget.tabCloseRequested.connect(self.CloseTab)

    def FindTable(self, fileName):
        for n in range(self.tabWidget.count()):
            if fileName == self.tabWidget.tabText(n).lower():
                table: [QTableWidget] = self.tabWidget.widget(n).findChild(QTableWidget)
                return table

        return None

    def UpdateScoreSheet(self):
        #  can only add subs if the current tabs is a score tab
        n = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(n)
        if 'score' not in name:
            QMessageBox.warning(None, "Error: not a score sheet", "Selected tab must be a score sheet")
            return

        n = self.tabWidget.currentIndex()
        table: QTableWidget = self.tabWidget.currentWidget().findChild(QTableWidget)

        for row in range(table.rowCount()-1 ,-1, -1):
            item = table.item(row,0)
            if not item:
                continue

            status = table.item(row,0).text()
            if status == 'x':
                table.removeRow(row)

        table.sortByColumn(1, QtCore.Qt.AscendingOrder)

        times = ['9:00', '10:15']

        color = QtGui.QColor(255, 242, 204)
        white = QtGui.QColor(255, 255, 255)
        colors = [color, white]
        for row in range(table.rowCount()):
            iclr = (row // 4) % 2
            # print('row ', row, (row // (4*6)) % 2, ' clr ', iclr)
            self.HiliteRow(table, row, colors[iclr])
            table.item(row, 4).setText(times[(row // (4*6)) % 2])

        table.resizeColumnsToContents()
        table.resizeRowsToContents()


    def CheckTable(self, msg, table):
        for i in range(table.rowCount()):
            if table.item(i,2):
                print(msg, i, table.item(i,2).text())
            else:
                print(msg, i, 'none -----')

            for j in range(table.columnCount()):
                item = table.item(i, j)
                if not item:
                    print(msg, i, j)


    def AddSubs(self):
        #  can only add subs if the current tabs is a score tab
        n = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(n)
        if 'score' not in name:
            QMessageBox.warning(None, "Error: not a score sheet", "You can only add subs to a score sheet")
            return

        subsTable: QTableWidget = self.FindTable('subs.csv')
        if not subsTable:
            QMessageBox.warning(None, "Open subs file", "Please open the 'subs.csv' file")
            loadCsv(self)
            return

        table: QTableWidget = self.tabWidget.currentWidget().findChild(QTableWidget)
        table.setSortingEnabled(False)

        self.CheckTable('before ', table)

        # remove all the subs that are in the current score sheet
        for row in range(table.rowCount()-1 ,-1, -1):
            name = table.item(row, 2).text()   # name is in 3rd col
            if '(sub)' in name:   # all subs have 
                table.removeRow(row)

        # add subs to score sheet until n players is divisible by 4
        for isub in range(subsTable.rowCount()):
            # if (table.rowCount() % 4) == 0:
            #     break

            # check if current sub is ready to play
            item1 = subsTable.item(isub, 0)
            if item1 and item1.text():  # any mark in the status col means good to go
                table.insertRow(0)

                # status col is blank
                table.setItem(0, 0, QtWidgets.QTableWidgetItem(''))

                # add the rank
                item = subsTable.item(isub, ColHdrs.rank.value)
                rank = 999  # very bogus rank
                if item:
                    rank = float(subsTable.item(isub, 1).text())

                item2 = QtWidgets.QTableWidgetItem()
                item2.setData(QtCore.Qt.EditRole, rank)
                table.setItem(0, 1, item2)


                # add the name
                name = '(sub) ' + subsTable.item(isub, 2).text()
                table.setItem(0, 2, QtWidgets.QTableWidgetItem(name))


                # add the phone
                phone = subsTable.item(isub, 3).text()
                if not phone:
                    phone = '---'
                table.setItem(0, 3, QtWidgets.QTableWidgetItem(phone))

                # add some blanks
                table.setItem(0, 4, QtWidgets.QTableWidgetItem(''))
                table.setItem(0, 5, QtWidgets.QTableWidgetItem(''))
                table.setItem(0, 6, QtWidgets.QTableWidgetItem(''))
                table.setItem(0, 7, QtWidgets.QTableWidgetItem(''))

        self.UpdateScoreSheet()
        table.setSortingEnabled(True)


    def CopyTable(self):
        n = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(n)
        table = self.tabWidget.currentWidget().findChild(QTableWidget)

        CopyAsHtml(name, table)


    def IsFileOpen(self, name):
        names = []
        for itab in range(self.tabWidget.count()):
            names.append(self.tabWidget.tabText(itab))

        test = name in names
        print(test, name,names)

        return name in names

    def ScheduleNextMatches(self):
        n = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(n)
        if 'standings' not in name:
            msg = QMessageBox.warning(None,"Wrong tab selected", "Current tab must be a 'standings' tab")
            return

        plrHdr = ['Status','rank','Name','Phone']

        scoreHdr = ['Status','Rank','Name','Phone', 'time', 'game 1',' game 2','game 3']
        name = name.replace('standings','scores')
        rows = []
        rows.append(scoreHdr)

        # Load the players from the current tab
        plrTable: QTableWidget = self.tabWidget.currentWidget().findChild(QTableWidget)
        for irow in range(plrTable.rowCount()):
            if plrTable.item(irow, 0).text():   # remove any play with status != ''
                continue

            row = []
            for icol in range(plrTable.columnCount()):
                item = plrTable.item(irow, icol)
                if item:
                    row.append(item.text())
                else:
                    row.append('')

            # add some blanks
            row.extend(['','','',''])  # blanks for time and game scores
            rows.append(row)           # add the row to rows

        table: QTableWidget = self.MakeNewTab(name, rows)
        table.verticalHeader().setVisible(True)
        self.UpdateScoreSheet()


    def HiliteRow(self, table, row, color):
        for j in range(table.columnCount()):
            item = table.item(row, j)
            if item:
                # print('hilite', row, j, table.item(row, j).text())
                table.item(row, j).setBackground(color)


    def CloseTab(self, index):
        tab = self.tabWidget.widget(index)
        tab.deleteLater()
        self.tabWidget.removeTab(index)


    def OpenFile(self):
        loadCsv(self)

    def SaveFile(self):
        n = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(n)
        table = self.tabWidget.currentWidget().findChild(QTableWidget)

        SaveAsCsv(name, table)


    def UpdateScores(self):
        sessions = ['01.7.20', '01.14.20','01.21.20','01.28.20','02.4.20','02.11.20','02.18.20','02.25.20','','']

        # check that the current tab has scores
        n = self.tabWidget.currentIndex()
        name = self.tabWidget.tabText(n)
        if 'score' not in name:
            msg = QMessageBox.warning(None,"Wrong tab selected", "Current tab must be a 'score' tab")
            return

        # see if the corresponding 'player week.csv' file is open
        plrSheet = None

        scrWeek = re.search(r"\d+.\d+.\d+", name).group()
        for itab in range(1, self.tabWidget.count()):
            if itab == n:
                continue

            tabName = self.tabWidget.tabText(itab)
            plrWeek = re.search(r"\d+.\d+.\d+", tabName).group()

            if plrWeek and scrWeek == plrWeek:
                weekTab = self.tabWidget.widget(itab)
                plrSheet = weekTab.findChild(QTableWidget)
                break

        if not plrSheet:
            QMessageBox.warning(None, "Standings file missing",
                                      "The Standings file for week: " + scrWeek + " is not open")
            return

        try:
            nextWeek = sessions[sessions.index(plrWeek)+1]
        except ValueError:
            nextWeek = 'week x'

        scoreSheet = self.tabWidget.currentWidget().findChild(QTableWidget)
        UpdateScores(self, scoreSheet, plrSheet, nextWeek)


    def SetPlayers(self, playerList, table = None):
        if not table:
            table = self.tabWidget.currentWidget().findChild(QTableWidget)

        playerData = []
        for col in range(table.columnCount()):
            text = table.horizontalHeaderItem(col).text()
            playerData.append(text.lower())

        if 'name' not in playerData:
            return

        lookup = {}
        for i, hdrname in enumerate(playerData):
            lookup[hdrname] = i

        playerList.clear()

        # set all the variables of the plr that are present in the file
        for irow in range(table.rowCount()):
            row = []
            for icol in range(table.columnCount()):
                item = table.item(irow,icol)
                if item:
                    row.append(item.text())
                else:
                    row.append('')

            plr = PlayerType(row[lookup['name']])
            playerList[plr.name] = plr
            for var in vars(plr):
                if var in lookup:
                    setattr(plr, var, row[lookup[var]])


    def SavePlayers(self, Rows, ThePlayers):
        hdrNames = [x.lower() for x in Rows[0]]
        playerData = Rows[1:]

        if 'name' not in hdrNames:
            return

        lookup = {}
        for i, hdrname in enumerate(hdrNames):
            lookup[hdrname] = i

        # set all the variables of the plr that are present in the file
        for i, playerRow in enumerate(playerData):
            plr = PlayerType(playerRow[lookup['name']])
            ThePlayers[plr.name]= plr
            for var in vars(plr):
                if var in lookup:
                    setattr(plr, var, playerRow[lookup[var]])


    def MakeNewTab(self, name, Rows):

        # if (name.startswith('subs')):
        #     self. SavePlayers(Rows, AllSubs)
        #     AllSubs['fileName'] = name

        scoreSheet = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(scoreSheet.sizePolicy().hasHeightForWidth())
        scoreSheet.setSizePolicy(sizePolicy)
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, -1)
        table: QTableWidget = QtWidgets.QTableWidget()

        hdrNames = Rows[0]
        table.setColumnCount(len(hdrNames))
        table.setRowCount(len(Rows) -1)
        table.verticalHeader().setVisible(True)
        header = table.horizontalHeader()
        header.setFrameStyle(QFrame.Box | QFrame.Plain)
        header.setStyleSheet("QHeaderView::section { border-bottom: 1px solid gray; }")

        table.setHorizontalHeaderLabels(hdrNames)
        table.horizontalHeader().setCascadingSectionResizes(True)

        for irow, row in enumerate(Rows):
            if irow > 0:
                for icol, col in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(col)
                    if icol == ColHdrs.rank.value and col:
                            item = QtWidgets.QTableWidgetItem()
                            item.setData(QtCore.Qt.EditRole, float(col))

                    table.setItem(irow - 1, icol, item)

        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        table.resizeColumnsToContents()
        hLayout.addWidget(table)
        scoreSheet.setLayout(hLayout)
        n = self.tabWidget.insertTab(1, scoreSheet, name)
        self.tabWidget.setCurrentIndex(n)

        table.setSortingEnabled(True)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        if 'score' in name:
            self.UpdateScoreSheet()
        else:
            self.HiliteAlternateRows(table)

        return table

    def HiliteAlternateRows(self, table):
        color = QtGui.QColor(242, 242, 242)
        white = QtGui.QColor(255, 255, 255)
        colors = [color, white]
        for row in range(table.rowCount()):
            iclr = row  % 2
            self.HiliteRow(table, row, colors[iclr])

    def tableChanged(item, table):
        x = 0
