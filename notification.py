from PyQt5 import QtCore, QtGui, QtWidgets

def showNotif(textPesan):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    msgBox.setIcon(QtWidgets.QMessageBox.Critical)
    font = QtGui.QFont()
    font.setPointSize(10)
    msgBox.setFont(font)
    msgBox.setStyleSheet("QLabel{ color: red}")

    # msgBox.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    msgBox.setText(textPesan)
    msgBox.exec_()