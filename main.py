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
        
        self.readSettings()
        
        
        
    def readSettings(self):
        settings = QSettings("Phytax", "Phydent")
        position = settings.value("pos_settings", QPoint(200,200))
        size = settings.value("size_settings", QSize(400,400))
        self.resize(size)
        self.move(position)

    def writeSettings(self):
        settings = QSettings("Phytax", "Phydent")
        settings.setValue("pos_settings", self.pos())
        settings.setValue("size_settings", self.size())
    
    def closeEvent(self, event):
        self.writeSettings()
    
    # def close_event(self,event):
    #     self.settings

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
    
    @staticmethod
    def valueToBool(value):
        return value.lower() == 'true' if isinstance(value, str) else bool(value)
    
    def readSettings(self):
        settings = QSettings("Phytax", "Phydent")
        position = settings.value("pos_mainwindow", QPoint(200,200))
        size = settings.value("size_mainwindow", QSize(400,400))
        self.resize(size)
        self.move(position)
        productlabel1_check = self.valueToBool(settings.value("productlabel1check", False))
        productlabel2_check = self.valueToBool(settings.value("productlabel2check", False))
        productlabel3_check = self.valueToBool(settings.value("productlabel3check", False))
        productlabel4_check = self.valueToBool(settings.value("productlabel4check", False))
        productlabel5_check = self.valueToBool(settings.value("productlabel5check", False))
        
        
        #print(productlabel1_check)
        # for i in labels:
        #     if {i}_check == True:
        #         i = settings.value("{}".format(i))
        #         self.{i}.setText({i})
        #background_color = "lightgray"
        
        if productlabel1_check == True:
            productlabel1 = settings.value("productlabel1")
            self.productlabel1.setText(productlabel1)
            self.productlabel1.setStyleSheet("color: rgb(105, 138, 147);")
        else:
            self.productlabel1edit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : lightgray;"
                                            "color : gray;"
                                            "}")
            self.productlabel1.setText("")
            self.productlabel1edit.setReadOnly(True)
            
        if productlabel2_check == True:
            productlabel2 = settings.value("productlabel2")
            self.productlabel2.setText(productlabel2)
            self.productlabel2.setStyleSheet("color: rgb(105, 138, 147);")
        else:
            self.productlabel2edit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : lightgray;"
                                            "color : gray;"
                                            "}")
            self.productlabel2.setText("")
            self.productlabel2edit.setReadOnly(True)
        
        if productlabel3_check == True:
            productlabel3 = settings.value("productlabel3")
            self.productlabel3.setText(productlabel3)
            self.productlabel3.setStyleSheet("color: rgb(105, 138, 147);")
        else:
            self.productlabel3edit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : lightgray;"
                                            "color : gray;"
                                            "}")
            self.productlabel3.setText("")
            self.productlabel3edit.setReadOnly(True)
            
        if productlabel4_check == True:
            productlabel4 = settings.value("productlabel4")
            self.productlabel4.setText(productlabel4)
            self.productlabel4.setStyleSheet("color: rgb(105, 138, 147);")
        else:
            self.productlabel4edit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : lightgray;"
                                            "color : gray;"
                                            "}")
            self.productlabel4.setText("")
            self.productlabel4edit.setReadOnly(True)
            
        if productlabel5_check == True:
            productlabel5 = settings.value("productlabel5")
            self.productlabel5.setText(productlabel5)
            self.productlabel5.setStyleSheet("color: rgb(105, 138, 147);")
        else:
            self.productlabel5edit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : lightgray;"
                                            "color : gray;"
                                            "}")
            self.productlabel5.setText("")
            self.productlabel5edit.setReadOnly(True)
            
        
    
    def writeSettings(self):
        settings = QSettings("Phytax", "Phydent")
        settings.setValue("pos_mainwindow", self.mainwindow_app.pos())
        settings.setValue("size_mainwindow", self.mainwindow_app.size())
        
    def __init__(self, parent=None):
        settings = QSettings("Phytax", "Phydent")
        self.mainwindow_app = super(mainwindow, self)
        self.mainwindow_app.__init__(parent)
        self.setupUi(self)
        # showTitle = self.valueToBool(settings.value('Settings/showTitle', True))
        #self.showTitleCheckBox.setChecked(showTitle)

        #self.mainwindow_app.closeEvent = self.closeEvent
        
        self.readSettings()
        
        # try: 
        #     self.resize(self.settings.value('window size'))
        #     self.move(self.settings.value('window position'))
        #     print(self.settings.value('test'))
        # except:
        #     pass
        
        
        # WHEN HIDE/SHOW METHOD ENABLED
        #self.measurementwindow = measurement()
        #self.settingswindow = settings()
        
        self.aboutwindow = about()
        self.loginwindow = login()

        self.startmeasurementbutton.clicked.connect(self.measurementstart)
        #self.actionEinstellungen.triggered.connect(self.open_settings)

        self.startmeasurementbutton_2.clicked.connect(self.exitapp)
        
        self.actionEinstellungen.triggered.connect(self.open_settingswindow)

        #self.startmeasurementbutton.clicked.connect(self.toggle_measurementwindow)

        # SHOULD NOT CAUSE MEMORY LEAKAGE DUE TO HIDE/SHOW
        # self.actionEinstellungen.triggered.connect(self.toggle_settingswindow)
        
        self.actionAbout.triggered.connect(self.toggle_about)

        self.popups = []
    
    def closeEvent(self, event):
        self.writeSettings()
        #print("Test")
        
    def open_settingswindow(self, checked):
        self.settingswindow = settings()
        self.settingswindow.show()
        
        settings_data = QSettings("Phytax", "Phydent")
        
        self.settingswindow.cancel_button.clicked.connect(self.go_back_settings)
        self.settingswindow.save_button.clicked.connect(self.save_application_settings)
        
        productlabel1_check = self.valueToBool( settings_data.value("productlabel1check", False))
        productlabel2_check = self.valueToBool( settings_data.value("productlabel2check", False))
        productlabel3_check = self.valueToBool( settings_data.value("productlabel3check", False))
        productlabel4_check = self.valueToBool( settings_data.value("productlabel4check", False))
        productlabel5_check = self.valueToBool( settings_data.value("productlabel5check", False))
        
        
        #print(productlabel1_check)
        # for i in labels:
        #     if {i}_check == True:
        #         i = settings.value("{}".format(i))
        #         self.{i}.setText({i})
        #background_color = "lightgray"
    
        self.settingswindow.productlabel1check.setChecked(productlabel1_check)
        productlabel1 =  settings_data.value("productlabel1")
        self.settingswindow.productlabel1edit.setText(productlabel1)
        self.settingswindow.productlabel1edit.setStyleSheet("color: rgb(105, 138, 147);")
        

        self.settingswindow.productlabel2check.setChecked(productlabel2_check)
        productlabel2 =  settings_data.value("productlabel2")
        self.settingswindow.productlabel2edit.setText(productlabel2)
        self.settingswindow.productlabel2edit.setStyleSheet("color: rgb(105, 138, 147);")
    
    
        self.settingswindow.productlabel3check.setChecked(productlabel3_check)
        productlabel3 =  settings_data.value("productlabel3")
        self.settingswindow.productlabel3edit.setText(productlabel3)
        self.settingswindow.productlabel3edit.setStyleSheet("color: rgb(105, 138, 147);")
        
        self.settingswindow.productlabel4check.setChecked(productlabel4_check)
        productlabel4 =  settings_data.value("productlabel4")
        self.settingswindow.productlabel4edit.setText(productlabel4)
        self.settingswindow.productlabel4edit.setStyleSheet("color: rgb(105, 138, 147);")

        self.settingswindow.productlabel5check.setChecked(productlabel5_check)
        productlabel5 =  settings_data.value("productlabel5")
        self.settingswindow.productlabel5edit.setText(productlabel5)
        self.settingswindow.productlabel5edit.setStyleSheet("color: rgb(105, 138, 147);")

        
        self.mainwindow_app.close()
        
    def go_back_settings(self):
        
    
        w = mainwindow()
        w.show()
        self.settingswindow.close()
        
    
    def save_application_settings(self):
        settings = QSettings("Phytax", "Phydent")
        
        if self.settingswindow.productlabel1check.isChecked() == True:
            settings.setValue("productlabel1check", True)
            settings.setValue("productlabel1", self.settingswindow.productlabel1edit.text())
            print("Value prodlabel1_checked saved as true")
        if self.settingswindow.productlabel1check.isChecked() == False:
            settings.setValue("productlabel1check", False)
            settings.setValue("productlabel1", self.settingswindow.productlabel1edit.text())
            print("Value prodlabel1_checked saved as false")
            
                         
        if self.settingswindow.productlabel2check.isChecked() == True:
            settings.setValue("productlabel2check", True)
            settings.setValue("productlabel2", self.settingswindow.productlabel2edit.text())
            print("Value prodlabel2_checked saved")
        
        if self.settingswindow.productlabel2check.isChecked() == False:
            settings.setValue("productlabel2check", False)
            settings.setValue("productlabel2", self.settingswindow.productlabel2edit.text())
            print("Value prodlabel2_checked saved as false")
            
            
        if self.settingswindow.productlabel3check.isChecked() == True:
            settings.setValue("productlabel3check", True)
            settings.setValue("productlabel3", self.settingswindow.productlabel3edit.text())
            print("Value prodlabel3_checked saved")
        
        if self.settingswindow.productlabel3check.isChecked() == False:
            settings.setValue("productlabel3check", False)
            settings.setValue("productlabel3", self.settingswindow.productlabel3edit.text())
            print("Value prodlabel3_checked saved as false")
            
            
        if self.settingswindow.productlabel4check.isChecked() == True:
            settings.setValue("productlabel4check", True)
            settings.setValue("productlabel4", self.settingswindow.productlabel4edit.text())
            print("Value prodlabel4_checked saved")
        
        if self.settingswindow.productlabel4check.isChecked() == False:
            settings.setValue("productlabel4check", False)
            settings.setValue("productlabel4", self.settingswindow.productlabel4edit.text())
            print("Value prodlabel4_checked saved as false")
                 
                 
        if self.settingswindow.productlabel5check.isChecked() == True:
            settings.setValue("productlabel5check", True)
            settings.setValue("productlabel5", self.settingswindow.productlabel5edit.text())
            print("Value prodlabel5_checked saved")
        
        if self.settingswindow.productlabel5check.isChecked() == False:
            settings.setValue("productlabel5check", False)
            settings.setValue("productlabel5", self.settingswindow.productlabel5edit.text())
            print("Value prodlabel5_checked saved as false")
            
        w = mainwindow()
        w.show()
        self.settingswindow.close()
        
    
    def toggle_about(self, checked):
        if self.aboutwindow.isVisible():
            self.aboutwindow.hide()
        else:
            self.aboutwindow.show()

    # def toggle_settingswindow(self, checked):
    #     if self.settingswindow.isVisible():
    #         self.settingswindow.hide()
    #     else:
    #         self.settingswindow.show()

    # def toggle_measurementwindow(self, checked):
    #     if self.measurementwindow.isVisible():
    #         self.measurementwindow.hide()
    #     else:
    #         self.measurementwindow.show()

    def go_back(self):
        self.measurementwindow.close()
        self.mainwindow_app.show()
        

    def measurementstart(self):
        settings = QSettings("Phytax", "Phydent")
        
         # Instantiate measurement class 
        self.measurementwindow = measurement()
        
        productlabel1 = self.productlabel1edit.text()
        productlabel2 = self.productlabel2edit.text()
        productlabel3 = self.productlabel3edit.text()
        productlabel4 = self.productlabel4edit.text()
        productlabel5 = self.productlabel5edit.text()
        
        
        productlabel1_check = self.valueToBool(settings.value("productlabel1check", False))
        productlabel2_check = self.valueToBool(settings.value("productlabel2check", False))
        productlabel3_check = self.valueToBool(settings.value("productlabel3check", False))
        productlabel4_check = self.valueToBool(settings.value("productlabel4check", False))
        productlabel5_check = self.valueToBool(settings.value("productlabel5check", False))

              
        self.measurementwindow.productlabel1edit.setReadOnly(True)
        self.measurementwindow.productlabel2edit.setReadOnly(True)
        self.measurementwindow.productlabel3edit.setReadOnly(True)
        self.measurementwindow.productlabel4edit.setReadOnly(True)
        self.measurementwindow.productlabel5edit.setReadOnly(True)
        
                 
        self.measurementwindow.productlabel1.setText(settings.value("productlabel1"))
        self.measurementwindow.productlabel2.setText(settings.value("productlabel2"))
        self.measurementwindow.productlabel3.setText(settings.value("productlabel3"))
        self.measurementwindow.productlabel4.setText(settings.value("productlabel4"))
        self.measurementwindow.productlabel5.setText(settings.value("productlabel5"))
        
        if productlabel1_check == False:
            self.measurementwindow.productlabel1.setText("")
            self.measurementwindow.productlabel1edit.setHidden(True)

        if productlabel2_check == False:
            self.measurementwindow.productlabel2.setText("")
            self.measurementwindow.productlabel2edit.setHidden(True)
        if productlabel3_check == False:
            self.measurementwindow.productlabel3.setText("")
            self.measurementwindow.productlabel3edit.setHidden(True)
        if productlabel4_check == False:
            self.measurementwindow.productlabel4.setText("")
            self.measurementwindow.productlabel4edit.setHidden(True)
        if productlabel5_check == False:
            self.measurementwindow.productlabel5.setText("")
            self.measurementwindow.productlabel5edit.setHidden(True)
        
        self.measurementwindow.productlabel1edit.setText(productlabel1)
        self.measurementwindow.productlabel2edit.setText(productlabel2)
        self.measurementwindow.productlabel3edit.setText(productlabel3)
        self.measurementwindow.productlabel4edit.setText(productlabel4)
        self.measurementwindow.productlabel5edit.setText(productlabel5)

 
        
        self.measurementwindow.productlabel1.setStyleSheet("color: rgb(105, 138, 147);")
        self.measurementwindow.productlabel2.setStyleSheet("color: rgb(105, 138, 147);")
        self.measurementwindow.productlabel3.setStyleSheet("color: rgb(105, 138, 147);")
        self.measurementwindow.productlabel4.setStyleSheet("color: rgb(105, 138, 147);")
        self.measurementwindow.productlabel5.setStyleSheet("color: rgb(105, 138, 147);")
        
        
        self.measurementwindow.productlabel1edit.setStyleSheet("QLineEdit"
                                            "{"
                                            #"background : lightgray;"
                                            "color : gray;"
                                            "}")
        self.measurementwindow.productlabel2edit.setStyleSheet("QLineEdit"
                                            "{"
                                            #"background : lightgray;"
                                            "color : gray;"
                                            "}")
        self.measurementwindow.productlabel3edit.setStyleSheet("QLineEdit"
                                            "{"
                                            #"background : lightgray;"
                                            "color : gray;"
                                            "}")
        self.measurementwindow.productlabel4edit.setStyleSheet("QLineEdit"
                                            "{"
                                            #"background : lightgray;"
                                            "color : gray;"
                                            "}")
        self.measurementwindow.productlabel5edit.setStyleSheet("QLineEdit"
                                            "{"
                                            #"background : lightgray;"
                                            "color : gray;"
                                            "}")
        
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
