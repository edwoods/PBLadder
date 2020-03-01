from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QApplication

scoreIntro = '''<html>
<body>
<!--StartFragment--><table align="center" border="2" style="color: rgb(0, 0, 0); font-family: &quot;Times New Roman&quot;; font-size: small; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">'''

playerIntro = '''<html>
<body>
<!--StartFragment--><table align="center" border="1" style="color: rgb(0, 0, 0); font-family: &quot;Times New Roman&quot;; font-size: small; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-style: initial; text-decoration-color: initial;">'''


def CopyAsHtml(tableName, table):
    # table = QtWidgets.QTableWidget()

    hdrColors = ['"lightcyan"', '"aqua"']  # 1st for player, 2nd for scores
    fontColors = [['"#000000"','"#000000"',],   # player font is black
                ['"#ffff99"', '"#ffffff"']]     # score font is black or dark red

    BgColors = [[ '"#ffffff"',  '"#e0e0e0"'],    # player bg is white
        ['"#ffff99"', '"#ffffff"']]             # score alternate every 4 rows: yellowish, white

    intros = [playerIntro, scoreIntro]

    tType = 0
    if 'score' in tableName:
        tType = 1

    html = intros[tType]
    html += '<tbody><tr bgcolor=' + hdrColors[tType] + '>'

    # column headers
    plainText = ''
    for col in range(1,table.columnCount()):
        name = table.horizontalHeaderItem(col).text()
        html += '<th>' + name + '</th>'
        plainText += name + ','

    html += '</tr>'
    plainText = plainText[:-1]  # remove last ','

    #  table rows
    for row in range(table.rowCount()):

        if tType == 1:   # score table
            irow = (row // 4) % 2
            html += '<tr bgcolor=' + BgColors[tType][irow] + '; ' + 'font color=' + fontColors[tType][irow] + '>'
        else:   # hilite alternate rows
            irow = row % 2
            html += '<tr bgcolor=' + BgColors[tType][irow] + '; ' + 'font color=' + fontColors[tType][irow] + '>'

        for col in range(1, table.columnCount()):
            name = table.item(row,col).text()
            html += '<td>' + name + '</td>'
            plainText += name + ','
        html += '</tr>'

        plainText = plainText[:-1] + '\n'

    html += '</tbody></table></body></html>'

    mimeData = QMimeData()
    mimeData.setHtml(html)
    mimeData.setText(plainText)
    clipboard = QApplication.clipboard()
    clipboard.setMimeData(mimeData)
