# Main Python file for the Phydent Application
import sys
import subprocess
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.uic.uiparser import QtWidgets

from PyQt5.QtWidgets import QDialog, QMainWindow

#from PyQt5 import QtCore, QtGui, QtWidgets
#from measurementUI import Ui_MainWindow
#from loginUI import Ui_Dialog
#from mainwindowUI import Ui_Messungen
#from loginMainWindowUI import Ui_MainWindow


# Import different window classes
import measurementUI
#import loginUI_old
import mainwindowUI
import settingsUI
import aboutUI 
import loginUI



class about(QMainWindow, aboutUI.Ui_MainWindow):
    def __init__(self, parent = None):
        super(about, self).__init__(parent)
        self.setupUi(self)


class settings(QMainWindow, settingsUI.Ui_Einstellungen):
    def __init__(self, parent = None):
        super(settings, self).__init__(parent)
        self.setupUi(self)

class measurement(QMainWindow, measurementUI.Ui_MainWindow):

    def __init__(self, parent=None):
        super(measurement, self).__init__(parent)
        self.setupUi(self)

        # self.productlabel1edit.setText(self.productlabel1var)  
        # self.productlabel2edit.setText(self.productlabel2var)
        # self.productlabel3edit.setText(self.productlabel3var)
        # self.productlabel4edit.setText(self.productlabel4var)

    
        
        

    #def go_back(self):
        
        #self.loginbutton.clicked.connect(self.login)
        #self.popups = []

class login(QMainWindow, loginUI.Ui_login):
    def __init__(self, parent=None):
        super(login, self).__init__(parent)
        self.setupUi(self)
        self.passinput.setEchoMode(QLineEdit.Password)
        self.loginbutton.clicked.connect(self.login)
        self.exitbutton.clicked.connect(self.exit_app)
        self.popups = []

    #@QtCore.pyqtSlot()
    def login(self):
        # print("clicked")
        user = self.userinput.text()
        password = self.passinput.text()
        path_to_opus = 'C:\Program Files\Bruker\OPUS_8.7.10/opus.exe'
        subprocess.Popen(['C:\Program Files\Bruker\OPUS_8.7.10/opus.exe','/Language=ENGLISH/OPUSPIPE=ON/HTTPSERVER=ON/HTTPPORT=80/DIRECTLOGINPASSWORD={}@{}'.format(user, password)])
        popwindow = mainwindow()
        popwindow.show()
        self.popups.append(popwindow)
        w.hide()

    def exit_app(self):
        sys.exit()

class mainwindow(QMainWindow, mainwindowUI.Ui_Messungen):
    def __init__(self, parent=None):
        self.mainwindow_app = super(mainwindow, self)
        self.mainwindow_app.__init__(parent)
        self.setupUi(self)

        #self.measurementwindow = measurement()
        self.settingswindow = settings()
        self.aboutwindow = about()
        self.loginwindow = login()

        self.startmeasurementbutton.clicked.connect(self.measurementstart)
        #self.actionEinstellungen.triggered.connect(self.open_settings)

        self.startmeasurementbutton_2.clicked.connect(self.exitapp)

        #self.startmeasurementbutton.clicked.connect(self.toggle_measurementwindow)

        # SHOULD NOT CAUSE MEMORY LEAKAGE DUE TO HIDE/SHOW
        self.actionEinstellungen.triggered.connect(self.toggle_settingswindow)
        # self.actionAbout.triggered.connect(self.open_about)
        self.actionAbout.triggered.connect(self.toggle_about)
        # self.actionEinstellungen.triggered.connect(self.)

        self.popups = []
    
    def toggle_about(self, checked):
        if self.aboutwindow.isVisible():
            self.aboutwindow.hide()
        else:
            self.aboutwindow.show()

    def toggle_settingswindow(self, checked):
        if self.settingswindow.isVisible():
            self.settingswindow.hide()
        else:
            self.settingswindow.show()

    def toggle_measurementwindow(self, checked):
        if self.measurementwindow.isVisible():
            self.measurementwindow.hide()
        else:
            self.measurementwindow.show()

    def go_back(self):
        self.measurementwindow.close()
        self.mainwindow_app.show()
        

    def measurementstart(self):
        productlabel1 = self.productlabel1edit.text()
        productlabel2 = self.productlabel2edit.text()
        productlabel3 = self.productlabel3edit.text()
        productlabel4 = self.productlabel4edit.text()
        productlabel5 = self.productlabel5edit.text()

        # Instantiate measurement class 
        self.measurementwindow = measurement()
        
        self.measurementwindow.productlabel1edit.setText(productlabel1)
        self.measurementwindow.productlabel2edit.setText(productlabel2)
        self.measurementwindow.productlabel3edit.setText(productlabel3)
        self.measurementwindow.productlabel4edit.setText(productlabel4)
        self.measurementwindow.productlabel5edit.setText(productlabel5)

        self.measurementwindow.productlabel1edit.setReadOnly(True)
        self.measurementwindow.productlabel2edit.setReadOnly(True)
        self.measurementwindow.productlabel3edit.setReadOnly(True)
        self.measurementwindow.productlabel4edit.setReadOnly(True)
        self.measurementwindow.productlabel5edit.setReadOnly(True)
        
        #labels = [productlabel1edit, productlabel2edit, productlabel3edit, productlabel4edit]
    
    
        self.measurementwindow.productlabel1edit.setStyleSheet("QLineEdit"
                                            "{"
                                            #"background : lightgray;"
                                            "color : gray;"
                                            "}")
        # measurementwindow.productlabel1edit = self.productlabel1
        # measurementwindow.productlabel2edit = self.productlabel2
        # measurementwindow.productlabel3edit = self.productlabel3
        # measurementwindow.productlabel4edit = self.productlabel4

        # measurementwindow.productlabel4edit = "Test"
        
        self.measurementwindow.backbutton.clicked.connect(self.go_back)
        
        self.measurementwindow.show()
        self.popups.append(self.measurementwindow)
        self.mainwindow_app.hide()
        print(self.popups)
    
    def exitapp(self):
        if self.measurementwindow.isVisible():
            # dlg = QDialog(self)
            # dlg.setWindowTitle("Test")
            # dlg.label = QLabel
            # dlg.exec()
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Test")
            dlg.setText("Eine Messung ist momentan am Laufen, wollen Sie die Anwendung wirklich schlissen")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            #dlg.addButton("test")
            dlg.button
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                print("Close Application")
                sys.exit()
            else:
                print("Close Dialog")
                dlg.close()
        else:
            sys.exit()
        
            # sys.exit()
    
    def open_settings(self):
        popwindow = settings()
        popwindow.show()
        self.popups.append(popwindow)

    def open_about(self):
        popwindow = about()
        popwindow.show()
        self.popups.append(about)


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


# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     w = mainwindow()
#     w.show()
#     sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = login()
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
