from PyQt5.QtGui import QPixmap, QPainter, QTextDocument, QTextCursor, QTextTableFormat, QTextCharFormat, QBrush, QColor
from PyQt5.QtPrintSupport import QPrinter

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from enum import Enum


class ColHdrs(Enum):
    status = 0
    rank = 1
    name = 2
    phone = 3


class PlayerType(object):
    def __init__(self, name, phone='', email='', rank=-1):
        self.name = name
        self.phone = phone
        self.email = email
        self.rank = rank
        self.history = []
        self.status = ''


def UpdateScores(MainWindow, ScoreTable, standingsTable, nextSession):
    """
    :type ScoreTable: QTableWidget
    :type standingsTable: QTableWidget
    """
    if ScoreTable.columnCount() != 8:
        QMessageBox.warning(None, "Score Table error",
                            "The Score Table has already been processed")
        return

    # make sure that the score table is filled in
    for row in range(ScoreTable.rowCount()):
        for col in range(5,8):
            item = ScoreTable.item(row, col)
            if not item:
                QMessageBox.warning(None, "Score Table error",
                    'No value in row,col: ' +  str(row+1) + ' ' + str(col+1))
                return
            else:
                try:
                    x = int(item.text())
                except ValueError:
                    QMessageBox.warning(None, "Score Table error",
                      'The value "' + item.text() + '" must be an int. in row:col ' + str(row + 1) + ':' + str(col + 1))
                    return

    # load the ldr player name from the plrTable tab
    ldrPlrNames = [standingsTable.item(i, 2).text() for i in range(standingsTable.rowCount())]
    ldrPlrRanks = [standingsTable.item(i, 1).text() for i in range(standingsTable.rowCount())]

    plrTblInfo = {}
    for i in range(standingsTable.rowCount()):
        row = []
        for icol in range(standingsTable.columnCount()):
            row.append(standingsTable.item(i, icol).text())
        plrTblInfo[ldrPlrNames[i]] = row

    # load the names of players that played this week
    curPlrNames = [ScoreTable.item(i, 2).text() for i in range(ScoreTable.rowCount())]

    # load the scores from the score tab
    nrows = ScoreTable.rowCount()
    ncols = ScoreTable.columnCount()

    scrHeaders = [str(ScoreTable.horizontalHeaderItem(i).text()) for i in range(ncols)]
    scrHeaders.extend(['oldRank', 'dScore', 'Order'])

    ScoreTable.setColumnCount(len(scrHeaders))
    ScoreTable.setHorizontalHeaderLabels(scrHeaders)

    AllRows = []
    for row in range(nrows):
        Row = []

        # grab the scores from cols 5,6,7
        for col in range(5, 8):
            item = ScoreTable.item(row, col)
            Row.append("0" if item is None else str(item.text()))
        AllRows.append(Row)

    for i in range(0, nrows, 4):  # 4 players per match
        matchScores = AllRows[i:i + 4]
        transpose = [*zip(*matchScores)]
        dscore = [0, 0, 0, 0]
        for game in range(3):
            scoresStr = transpose[game]
            scores = [int(i) for i in scoresStr]  # turn score to numbers
            hi: int = max(scores)
            lo: int = min(scores)

            for iplr in range(4):
                if int(matchScores[iplr][game]) == hi:
                    dscore[iplr] += hi - lo
                else:
                    dscore[iplr] -= hi - lo

        for iplr in range(4):
            matchScores[iplr].append(dscore[iplr])

    # compute the new rank for each active player
    rank = 1
    for i, plr in enumerate(AllRows):
        dscore = plr[-1]
        order = rank - dscore / 4
        plr.append(rank)
        plr.append(order)
        plr.insert(0, curPlrNames[i])

        item = QtWidgets.QTableWidgetItem(str(rank))
        ScoreTable.setItem(i, ncols + 0, item)

        item = QtWidgets.QTableWidgetItem(str(dscore))
        ScoreTable.setItem(i, ncols + 1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setData(QtCore.Qt.EditRole, order)
        ScoreTable.setItem(i, ncols + 2, item)

        if curPlrNames[i] in ldrPlrNames:
            rank += 1

    # add in the players who did not play
    for i, ldrPlrName in enumerate(ldrPlrNames):
        if ldrPlrName not in curPlrNames:
            rank = ldrPlrRanks[i]
            row = [ldrPlrName, '-', '-', '-', -4.4, int(rank), int(rank) + 4.4 / 4]
            AllRows.append(row)

    sortedByOrder = sorted(AllRows, key=lambda x: x[-1])

    subs = [plr for plr in sortedByOrder if plr[0] not in ldrPlrNames]
    actives = [plr for plr in sortedByOrder if plr[0] in ldrPlrNames]

    # create an list that for next weeks standings
    nwsHdr = ['Status', 'Rank', 'Name', 'Phone']
    ncols = standingsTable.columnCount()
    for i in range(ncols - 4 + 1, 0, -1):
        nwsHdr.append('W' + str(i))

    nextWeekStnds = [nwsHdr]
    for i, plr in enumerate(actives):
        upPlr = plrTblInfo[plr[0]]  # find the play old info
        upPlr[1] = i + 1            # set the new rank
        upPlr.insert(4, str(plr[5]) + ' : ' + str(plr[4]))
        nextWeekStnds.append(upPlr)

    MainWindow.MakeNewTab('standings ' + nextSession + '.csv', nextWeekStnds)

    ScoreTable.verticalHeader().setVisible(True)

    ScoreTable.resizeColumnsToContents()
    ScoreTable.resizeRowsToContents()


def SaveTableImage(table):
    pixmap = table.grab()
    pixmap.save("widget.png")
    SaveTableImage(table)

    nrows = table.rowCount()
    ncols = table.columnCount()
    doc = QTextDocument()
    cursor = QTextCursor(doc)
    tableFormat = QTextTableFormat()

    tableFormat.setHeaderRowCount(1)
    tableFormat.setAlignment(Qt.AlignHCenter)
    tableFormat.setCellPadding(0)
    tableFormat.setCellSpacing(0)
    tableFormat.setBorder(1)
    tableFormat.setBorderBrush(QBrush(Qt.SolidPattern))
    tableFormat.clearColumnWidthConstraints()

    textTable = cursor.insertTable(nrows + 1, ncols, tableFormat)
    tableHeaderFormat = QTextCharFormat()
    tableHeaderFormat.setBackground(QColor("#DADADA"))
    for i in range(ncols):
        cell = textTable.cellAt(0, i)
        cell.setFormat(tableHeaderFormat)
        cellCursor = cell.firstCursorPosition()
        cellCursor.insertText(table.horizontalHeaderItem(i).text())

    for i in range(nrows):
        for j in range(ncols):
            item = table.item(i, j)
            t = "" if item is None else str(item.text())
            # if item.text().iEmpty():
            #     table.setItem(i,j,QTableWidgetItem("0"))

            cell = textTable.cellAt(i + 1, j)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(t)

    cursor.movePosition(QTextCursor.End)
    printer = QPrinter(QPrinter.PrinterResolution)
    printer.setPaperSize(QPrinter.A4)
    printer.setOrientation(QPrinter.Landscape)
    printer.setOutputFileName("w8.pdf")
    doc.setDocumentMargin(0)
    doc.setTextWidth(5)
    doc.print(printer)
