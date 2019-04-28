import sys, json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import flogin, flistperizinan


class Controller:
    def __init__(self):
        self.login = flogin.Ui_Login()
        self.mainWindow = flistperizinan.Ui_TablePerizinan()

    def showLogin(self):
        self.login.switch_window.connect(self.showMainWindow)
        self.login.show()

    def showMainWindow(self):
        self.mainWindow.switch_window.connect(self.showLogin)
        if self.mainWindow.buildTable():
            self.mainWindow.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.showMainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
