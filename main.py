# Main Python file for the Phydent Application
import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.uic.uiparser import QtWidgets

from PyQt5.QtWidgets import QDialog, QMainWindow

#from PyQt5 import QtCore, QtGui, QtWidgets
from measurementUI import Ui_MainWindow
# from loginUI import Ui_Dialog
from mainwindowUI import Ui_Messungen
# from loginMainWindowUI import Ui_MainWindow

import measurementUI
import loginUI
import mainwindowUI


class measurement(QMainWindow, measurementUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(measurement, self).__init__(parent)
        self.setupUi(self)
        #self.loginbutton.clicked.connect(self.login)
        #self.popups = []

# class login(QMainWindow, loginUI.Ui_Dialog):
#     def __init__(self, parent=None):
#         super(login, self).__init__(parent)
#         self.setupUi(self)
#         self.loginbutton.clicked.connect(self.login)
#         self.popups = []

#     #@QtCore.pyqtSlot()
#     def login(self):
#         popwindow = mainwindow()
#         popwindow.show()
#         self.popups.append(popwindow)

class mainwindow(QMainWindow, mainwindowUI.Ui_Messungen):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.startmeasurementbutton.clicked.connect(self.measurementstart)
        self.startmeasurementbutton_2.clicked.connect(self.exitapp)
        self.popups = []

    def measurementstart(self):
        popwindow = measurement()
        popwindow.show()
        self.popups.append(popwindow)
    
    def exitapp(self):
        sys.exit()


# class BookPopoutWindow(QtWidgets.QMainWindow, bookPopout.BookPopout):
#     def __init__(self, parent=None):
#         super(BookPopoutWindow, self).__init__(parent)
#         self.setupUi(self)


# class MainMenu(QtWidgets.QMainWindow, mainmenu.Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(MainMenu, self).__init__(parent)
#         self.setupUi(self)
#         self.createNewBookButton.clicked.connect(self.openNewBook)
#         self.popups = []

#     @QtCore.pyqtSlot()
#     def openNewBook(self):
#         popWin = BookPopoutWindow()
#         popWin.show()
#         self.popups.append(popWin)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = mainwindow()
    w.show()
    sys.exit(app.exec_())


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     Dialog = QtWidgets.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())

    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    # MainWindow = QtWidgets.QMainWindow()
    # # As first window open the login prompt
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     Dialog = QtWidgets.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())

    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    # MainWindow = QtWidgets.QMainWindow()
    # # As first window open the login prompt
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
