# Main Python file for the Phydent Application
from cProfile import label
from codecs import ignore_errors
from concurrent.futures import process
from brukeropusreader import read_file
import sys
import os
import time
from datetime import datetime
import sys
import subprocess
from pathlib import Path
from unicodedata import name
import numpy as np
import pandas as pd
from typing import Text

from fpdf import FPDF
import socket
import os

import matplotlib

#from OPUS_reader_test import opusrequest
matplotlib.use('Agg')
import matplotlib.pyplot as plt


'Import NN relevant Packages'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import LabelEncoder
# from keras.utils import to_categorical
import keras as ks

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.uic.uiparser import QtWidgets
import numpy
import pyqtgraph as pg
from pyqtgraph import PlotWidget , plot

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
import OPUS
from OPUS import opusrequest

# import OPUS_communication

class GlobalStandardScaler(object):
    """Scales to unit standard deviation and mean centering using global mean and std of X, sklearn like API"""
    def __init__(self,with_mean=True, with_std=True, normfact=1.0):
        self._with_mean = with_mean
        self._with_std = with_std
        self.std = None
        self.normfact=normfact
        self.mean = None
        self._fitted = False
        
    def fit(self,X, y = None):
        X = np.array(X)
        self.mean = X.mean()
        self.std = X.std()
        self._fitted = True
        
    def transform(self,X, y=None):
        if self._fitted:
            X = np.array(X)
            if self._with_mean:
                X=X-self.mean
            if self._with_std:
                X=X/(self.std*self.normfact)
            return X
        else:
            print("Scaler is not fitted")
            return
            
    def inverse_transform(self,X, y=None):
        if self._fitted:
            X = np.array(X)
            if self._with_std:
                X=X*self.std*self.normfact
            if self._with_mean:
                X=X+self.mean
            return X
        else:
            print("Scaler is not fitted")
            return
            
    def fit_transform(self,X, y=None):
        self.fit(X)
        return self.transform(X)


class about(QMainWindow, aboutUI.Ui_About):
    def __init__(self, parent = None):
        super(about, self).__init__(parent)
        self.setupUi(self)


class settings(QMainWindow, settingsUI.Ui_Einstellungen):
    settings_data = QSettings("Phytax", "Phydent")
    def __init__(self, parent = None):
        settings_data = QSettings("Phytax", "Phydent")
        super(settings, self).__init__(parent)
        self.setupUi(self)
        
        self.readSettings()
        
        self.logdatei_edit.setText(settings_data.value("log_path"))
        self.messsdaten_edit.setText(settings_data.value("data_path"))
        self.report_edit.setText(settings_data.value("report_path"))
        # QComboBox has no attribute 'setText'
        #self.NN_choose_drop.setText(settings_data.value("NNmodel_path"))
        
        
    def readSettings(self):
        position = self.settings_data.value("pos_settings", QPoint(200,200))
        size = self.settings_data.value("size_settings", QSize(400,400))
        self.resize(size)
        self.move(position)

    def writeSettings(self):
        settings = QSettings("Phytax", "Phydent")
        settings.setValue("pos_settings", self.pos())
        settings.setValue("size_settings", self.size())
    
    def closeEvent(self, event):
        self.writeSettings()
        # result = isinstance(self.thread, QThread)
        # print("The background_measurement exists: {}".format(result))
        # if self.background_measurement_thread == True:
        #     dlg = QMessageBox(self)
        #     dlg.setText("Eine Hintergrundmessung ist momentan am Laufen, wollen Sie die Anwendung wirklich schliessen")
        #     dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #     #dlg.addButton("test")
        #     dlg.button
        #     dlg.setIcon(QMessageBox.Information)
        #     button = dlg.exec()

        #     if button == QMessageBox.Yes:
        #         print("Close Application")
        #         os.system("TASKKILL /F /IM opus.exe")
        #         sys.exit()
        #     else:
        #         print("Close Dialog")
        #         dlg.close()
        
        # else:
        #     os.system("TASKKILL /F /IM opus.exe")
        #     sys.exit()
        
        
    
    # def close_event(self,event):
    #     self.settings

class measurement(QMainWindow, measurementUI.Ui_MainWindow):

    @staticmethod
    def valueToBool(value):
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    class_instantiated = False

    label_color = 'rgb(34, 34, 34)'

    # def go_back(self):
    #     if self.thread.isRunning():
    #         print("its running")
    #         #print(self.thread)
    #         dlg = QMessageBox(self)
    #         dlg.setText("Eine Messung ist momentan am Laufen, wollen Sie diese wirklich unterbrechen?")
    #         dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    #         #dlg.addButton("test")
    #         dlg.button
    #         dlg.setIcon(QMessageBox.Information)
    #         button = dlg.exec()

    #         if button == QMessageBox.Yes:
    #             print("Going back")
    #             self.hide()
    #             self.mainwindow.show()
    #         else:
    #             print("Close Dialog")
    #             dlg.close()
    #     else:
    #         print("it's not running")
    
    
    # def opus_metadata():

    

    def __init__(self, productlabel1, productlabel2, productlabel3, productlabel4, productlabel5, mainwindow, parent = None):
        super(measurement, self).__init__(parent)
        self.setupUi(self)
        self.mainwindow = mainwindow

        settings = QSettings("Phytax", "Phydent")

        # self.productlabel1 = productlabel1
        # self.productlabel2 = productlabel2
        # self.productlabel3 = productlabel3
        # self.productlabel4 = productlabel4
        # self.productlabel5 = productlabel5


        productlabel1_check = self.valueToBool(settings.value("productlabel1check", False))
        productlabel2_check = self.valueToBool(settings.value("productlabel2check", False))
        productlabel3_check = self.valueToBool(settings.value("productlabel3check", False))
        productlabel4_check = self.valueToBool(settings.value("productlabel4check", False))
        productlabel5_check = self.valueToBool(settings.value("productlabel5check", False))

        self.productlabel1edit.setReadOnly(True)
        self.productlabel2edit.setReadOnly(True)
        self.productlabel3edit.setReadOnly(True)
        self.productlabel4edit.setReadOnly(True)
        self.productlabel5edit.setReadOnly(True)

        self.productlabel1.setText(settings.value("productlabel1"))
        self.productlabel2.setText(settings.value("productlabel2"))
        self.productlabel3.setText(settings.value("productlabel3"))
        self.productlabel4.setText(settings.value("productlabel4"))
        self.productlabel5.setText(settings.value("productlabel5"))

         
        if productlabel1_check == False:
            self.productlabel1.setText("")
            self.productlabel1edit.setHidden(True)
        if productlabel2_check == False:
            self.productlabel2.setText("")
            self.productlabel2edit.setHidden(True)
        if productlabel3_check == False:
            self.productlabel3.setText("")
            self.productlabel3edit.setHidden(True)
        if productlabel4_check == False:
            self.productlabel4.setText("")
            self.productlabel4edit.setHidden(True)
        if productlabel5_check == False:
            self.productlabel5.setText("")
            self.productlabel5edit.setHidden(True)


        self.productlabel1edit.setText(productlabel1)
        self.productlabel2edit.setText(productlabel2)
        self.productlabel3edit.setText(productlabel3)
        self.productlabel4edit.setText(productlabel4)
        self.productlabel5edit.setText(productlabel5)

        self.productlabel1.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel2.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel3.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel4.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel5.setStyleSheet("color: {};".format(self.label_color))


        self.productlabel1edit.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel2edit.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel3edit.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel4edit.setStyleSheet("color: {};".format(self.label_color))
        self.productlabel5edit.setStyleSheet("color: {};".format(self.label_color))

        #self.productlabel1edit.setText(log_prompt)

        self.class_instantiated = True

        self.printbutton.setEnabled(False)


        # self.productlabel1edit.setText(self.productlabel1var)  
        # self.productlabel2edit.setText(self.productlabel2var)
        # self.productlabel3edit.setText(self.productlabel3var)
        # self.productlabel4edit.setText(self.productlabel4var)

    #def go_back(self):
        
        #self.loginbutton.clicked.connect(self.login)
        #self.popups = []

class login(QMainWindow, loginUI.Ui_login):
    label_color = 'rgb(34, 34, 34)'
    settings_data = QSettings("Phytax", "Phydent")
    toplist = []
    winlist = []

    def __init__(self, parent=None):
        super(login, self).__init__(parent)
        self.setupUi(self)
        self.passinput.setEchoMode(QLineEdit.Password)
        self.loginbutton.clicked.connect(self.login)
        self.exitbutton.clicked.connect(self.exit_app)
        self.mainapplication = mainwindow()

        
        #self.mainapplication.backgroundbutton.clicked.connect(self.background_measurement_start)
        #self.popups = []
    def enum_callback(self,hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    def login(self):
        # print("clicked")
        user = self.userinput.text()
        password = self.passinput.text()

        path_to_opus = 'C:\Program Files\Bruker\OPUS_8.7.10/opus.exe'
        subprocess.Popen(['C:\Program Files\Bruker\OPUS_8.7.10/opus.exe','/Language=ENGLISH/OPUSPIPE=ON/HTTPSERVER=ON/HTTPPORT=80/DIRECTLOGINPASSWORD={}@{}'.format(user, password)])

        # win32gui.EnumWindows(self.enum_callback, self.toplist)
        # opus = [(hwnd, title) for hwnd, title in self.winlist if 'opus' in title.lower()]
        # win32gui.ShowWindow(opus[0], win32con.SW_MINIMIZE)
                
        # popwindow = mainwindow()
        #time.sleep(3)

        self.mainapplication.show()
        #self.popups.append(popwindow)
        w.close()
    
    # def background_measurement_start(self):
    #     settings = QSettings("Phytax", "Phydent")
    #     path = settings.value("data_path")
    #     print(path)
    #     background = OPUS_communication.opusrequest("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})".format(path))
    #     current_time = time.ctime()
    #     print(background)
    #     print(current_time)
    #     settings.setValue("last_bckgr", "Letzte Hintergrundmessung: {}".format(current_time))
    #     #self.mainapplication.__init__
    #     self.mainapplication.__init__
    #     #self.mainapplication.lastbackgroundmeasurementlabel.update()
    #     #self.mainapplication.lastbackgroundmeasurementlabel.repaint()
    #     #self.mainapplication.lastbackgroundmeasurementlabel.setAttribute(Qt.WA_StyledBackground, True)
    #     #currentwindow = self.popups[0]
        
    #     # reference=OPUS.opusrequest("127.0.0.1", 80, "MeasureReference(0, {EXP='ATR_Di.XPM', XPP='/mnt/c/Users/G164.PHYTAX/Desktop/phydent/', NSR=10})")
        
    #     print("Test")

    def exit_app(self):
        sys.exit()

class mainwindow(QMainWindow, mainwindowUI.Ui_Messungen):
    label_color = 'rgb(34, 34, 34)'
    
    settings_data = QSettings("Phytax", "Phydent")
    background_measurement_thread = False
    
    # def refreshUI(self):
    #     self.mainwindow_app

    @staticmethod
    def valueToBool(value):
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    def writelastbackground_measurement(self):
        settings = QSettings("Phytax", "Phydent")
        current_time = time.ctime()
        settings.setValue("last_bckgr", "Letzte Hintergrundmessung: {}".format(current_time))
        self.lastbackgroundmeasurementlabel.setText(settings.value("last_bckgr"))
        #self.lastbackgroundmeasurementlabel.update()
        self.actionEinstellungen.setEnabled(True)
        self.startmeasurementbutton.setEnabled(True)
        self.backgroundbutton.setText("Hintergrundmessung")
        self.backgroundbutton.setEnabled(True)
        self.background_measurement_thread = False
        #self.__init__

    def background_measurement_start(self):
        settings = QSettings("Phytax", "Phydent")
        path = settings.value("data_path")
        print(path)
        # Create thread object
        # self.statusBar.showMessage("Hintegrundmessung in Fortschritt")
        self.backgroundbutton.setEnabled(False)
        self.backgroundbutton.setText("Hintergrundmessung läuft")
        self.startmeasurementbutton.setEnabled(False)
        self.actionEinstellungen.setEnabled(False)
        self.thread = QThread()
        self.background_measurement_thread = True
        # Create worker object, Instantiate class
        self.worker = OPUS.OPUS_coms()
        self.worker.path = path
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        #self.thread.started.connect(self.worker.opusrequest("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})"))
        #self.thread.started.connect(self.worker.opusrequest_fireandforget("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})".format(path)))
        self.worker.finished.connect(self.thread.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        #self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.r)
        self.thread.start()
        # self.thread.finished.connect(
        #     lambda: self.lastbackgroundmeasurementlabel.setText("Test")
        # )S

        self.thread.finished.connect(
           self.writelastbackground_measurement
        )
        
        #if self.thread.isFinished == True:
            #print("thread is finished")

        # self.backgroundbutton.setEnabled(False)
        # self.thread.finished.connect(
        #     lambda: self.backgroundbutton.setEnabled(True)
        # )
        #OPUS_communication.opusrequest_fireandforget("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})".format(path))
        # OPUS_communication.opusrequest("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})".format(path))
        

        # print(current_time)
        # settings.setValue("last_bckgr", "Letzte Hintergrundmessung: {}".format(current_time))
        # #self.mainapplication.__init__
        # self.lastbackgroundmeasurementlabel.setText(settings.value("last_bckgr"))
        # self.lastbackgroundmeasurementlabel.update()
        #self.__init__
    
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
            self.productlabel1.setStyleSheet("color: {};".format(self.label_color))
            self.productlabel1edit.setReadOnly(False)
            self.productlabel1edit.setStyleSheet("QLineEdit"
                                        "{"
                                        "background : white;"
                                        "color : %s;"
                                        "}" % (self.label_color))
        
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
            self.productlabel2.setStyleSheet("color: {};".format(self.label_color))
            self.productlabel2edit.setReadOnly(False)
            self.productlabel2edit.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : white;"
                                    "color : %s;"
                                    "}" % (self.label_color))
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
            self.productlabel3.setStyleSheet("color: {};".format(self.label_color))
            self.productlabel3edit.setReadOnly(False)
            self.productlabel3edit.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : white;"
                                    "color : %s;"
                                    "}" % (self.label_color))
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
            self.productlabel4.setStyleSheet("color: {};".format(self.label_color))
            self.productlabel4edit.setReadOnly(False)
            self.productlabel4edit.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : white;"
                                    "color : %s;"
                                    "}" % (self.label_color))
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
            self.productlabel5.setStyleSheet("color: {};".format(self.label_color))
            self.productlabel5edit.setReadOnly(False)
            self.productlabel5edit.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : white;"
                                    "color : %s;"
                                    "}" % (self.label_color))
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
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
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

        self.backgroundbutton.clicked.connect(self.background_measurement_start)
        
        self.aboutwindow = about()
        #self.loginwindow = login()

        self.startmeasurementbutton.clicked.connect(self.measurementstart)
        #self.actionEinstellungen.triggered.connect(self.open_settings)

        self.startmeasurementbutton_2.clicked.connect(self.exitapp)
        
        self.actionEinstellungen.triggered.connect(self.open_settingswindow)

        #self.startmeasurementbutton.clicked.connect(self.toggle_measurementwindow)

        # SHOULD NOT CAUSE MEMORY LEAKAGE DUE TO HIDE/SHOW
        # self.actionEinstellungen.triggered.connect(self.toggle_settingswindow)
        
        self.actionAbout.triggered.connect(self.toggle_about)
        self.lastbackgroundmeasurementlabel.setText(settings.value("last_bckgr"))
        print(settings.value("last_bckgr"))
        self.lastbackgroundmeasurementlabel.update()
        self.lastbackgroundmeasurementlabel.hide()
        self.lastbackgroundmeasurementlabel.show()

        self.popups = []
    
    def closeEvent(self, event):
        self.writeSettings()
        #print("Test")

    def select_NNmodel_path(self):
        dialog = QFileDialog()
        chosen_NNmodel_path = dialog.getExistingDirectory(None, "Select Folder")
        if chosen_NNmodel_path  != "":
            self.settings_data.setValue("NNmodel_path", chosen_NNmodel_path)
            self.settingswindow.NN_choose_drop.setText(self.settings_data.value("NNmodel_path"))
            self.settingswindow.__init__

    def select_report_path(self):
        #settings = QSettings("Phytax", "Phydent")
        #path = QFileDialog.getExistingDirectory(self, 'Select a Folder', '', 'All Files (*.*)')
        #path = QFileDialog.getExistingDirectory(None, 'Select a Folder', )
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        #folder_path = r"{}".format(folder_path)
        
        if folder_path != "":
            self.settings_data.setValue("report_path", folder_path)
            self.settingswindow.report_edit.setText(self.settings_data.value("report_path"))
            print(folder_path)
            self.settingswindow.__init__
        
    def select_data_path(self):
        #settings = QSettings("Phytax", "Phydent")
        #path = QFileDialog.getExistingDirectory(self, 'Select a Folder', '', 'All Files (*.*)')
        #path = QFileDialog.getExistingDirectory(None, 'Select a Folder', )
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        #folder_path = r"{}".format(folder_path)
        
        if folder_path != "":
            self.settings_data.setValue("data_path", folder_path)
            self.settingswindow.messsdaten_edit.setText(self.settings_data.value("data_path"))
            print(folder_path)
            self.settingswindow.__init__

   
    def select_log_path(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")

        if folder_path != "":
            self.settings_data.setValue("log_path", folder_path)
            self.settingswindow.logdatei_edit.setText(self.settings_data.value("log_path"))
            print(folder_path)
            self.settingswindow.__init__
        
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
        self.settingswindow.productlabel1edit.setStyleSheet("color: {};".format(self.label_color))
        

        self.settingswindow.productlabel2check.setChecked(productlabel2_check)
        productlabel2 =  settings_data.value("productlabel2")
        self.settingswindow.productlabel2edit.setText(productlabel2)
        self.settingswindow.productlabel2edit.setStyleSheet("color: {};".format(self.label_color))
    
    
        self.settingswindow.productlabel3check.setChecked(productlabel3_check)
        productlabel3 =  settings_data.value("productlabel3")
        self.settingswindow.productlabel3edit.setText(productlabel3)
        self.settingswindow.productlabel3edit.setStyleSheet("color: {};".format(self.label_color))
        
        self.settingswindow.productlabel4check.setChecked(productlabel4_check)
        productlabel4 =  settings_data.value("productlabel4")
        self.settingswindow.productlabel4edit.setText(productlabel4)
        self.settingswindow.productlabel4edit.setStyleSheet("color: {};".format(self.label_color))

        self.settingswindow.productlabel5check.setChecked(productlabel5_check)
        productlabel5 =  settings_data.value("productlabel5")
        self.settingswindow.productlabel5edit.setText(productlabel5)
        self.settingswindow.productlabel5edit.setStyleSheet("color: {};".format(self.label_color))

        
        self.settingswindow.messdaten_choose.clicked.connect(self.select_data_path)
        self.settingswindow.logdatei_choose.clicked.connect(self.select_log_path)
        self.settingswindow.report_choose.clicked.connect(self.select_report_path)

        #self.settingswindow.NN_choose_drop.clicked.connect(self.select_NNmodel_path)

        rel_path_phydent_models = "phydent_models"
        abs_path_phydent_models = os.path.abspath(rel_path_phydent_models)

        list_phydent_models = [name for name in os.listdir(abs_path_phydent_models) if os.path.isdir(os.path.join(abs_path_phydent_models, name)) ]
        print("Phydent models: {}".format(list_phydent_models))
        for i in list_phydent_models:
            self.settingswindow.NN_choose_drop.addItem("{}".format(i))

        current_text = self.settingswindow.NN_choose_drop.currentText()
        self.settingswindow.NN_choose_drop.currentIndexChanged.connect(self.selection_change_dropdown)
        #self.mainwindow_app.hide()
        self.mainwindow_app.close()


    def selection_change_dropdown(self,i):
        print("Current index",i,"selection changed ", self.settingswindow.NN_choose_drop.currentText())
        self.settings_data.setValue("chosenNNmodel", self.settingswindow.NN_choose_drop.currentText())
        
    def go_back_settings(self):
        
        print(self.thread)
        # w = mainwindow()
        # w.show()
        self.mainwindow_app.show()
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
            
        # self.mainwindow_app.__init__
        # self.mainwindow_app.setupUi
        # self.productlabel1.update()
        # self.productlabel1.hide()
        # self.productlabel1.show()

        """ALTERNATIVE FIX TO QTHREAD PROBLEM (HIDE/SHOW with restart on settings change)"""
        # cwdir = os.getcwd()
        # os.system("TASKKILL /F /IM opus.exe")
        # os.system('python "{}/main.py"'.format(cwdir))
        

        #sys.exit()
        # self.show()
        self.mainwindow_app.show()
        self.readSettings()
        # w = mainwindow()
        # w.show()
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

    # def go_back(self):
    #     self.measurementwindow.hide()
    #     self.mainwindow_app.show()

    def go_back(self):

        def process_return():
            # if os.path.exists('analysis_report/plot_spectra.png'):
            #     os.remove('analysis_report/plot_spectra.png')
            # else:
            #     print("Can not delete the file as it doesn't exists")
            path_file =opusrequest("127.0.0.1", 80,"GET_SELECTED")[1]
            opusrequest("127.0.0.1", 80,"UNLOAD_FILE {}".format(path_file))


        if self.thread.isRunning():
            print("its running")
            #print(self.thread)
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warnung")
            dlg.setText("Eine Messung ist momentan am Laufen, wollen Sie diese wirklich unterbrechen?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            #dlg.addButton("test")
            dlg.button
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                print("Going back")
                self.measurementwindow.hide()
                process_return()
                self.show()
            else:
                print("Close Dialog")
                dlg.close()
        else:
            self.measurementwindow.hide()
            process_return()
            self.show()

    # def plot_spectra(self):
        

    # def progress_measurement(self,value):
    #         self.measurementwindow.logPrompt.append("[{}]: Vorverarbeitung des Spektrums".format(self.gettime()))
    #         self.plot_spectra()


    def create_report_pdf(self, metadata, productlabels_items):
        
        spectrometer, version, operator, experiment_filename, method_filename, spectrum_filename, spectrum_pathname, identification, identification_result = metadata

        '''Parameter List Document'''
        height_list = 6
        width_list =  200
        baseline_start_height =  15
        margin_def = 15
        width_a4 = 210
        height_a4 = 297

        pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
        pdf.add_page()

        pdf.set_font("Arial", size = 9)
        pdf.set_xy(margin_def, baseline_start_height)
        pdf.set_line_width(0.0)

        pdf.set_right_margin(15)
        pdf.set_right_margin(15)

        f = open("analysis_report/Phytax_info.txt", "r")
        for x in f:
            #pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt='Phytax GmbH', border=0)
            pdf.cell(200, 4, txt = x, ln = 3, align = 'L')

        pdf.set_xy(0, baseline_start_height + 30)
        pdf.set_font("Arial",'B', size = 13 )
        pdf.cell(200, 10, "Report of Analysis", align = 'C')

        pdf.set_xy(margin_def, baseline_start_height + 50)
        pdf.set_font('Arial', size = 9)
        pdf.cell(ln = 3, h = height_list, w=width_list, txt = "Spectrometer: {}".format(spectrometer))
        pdf.cell(ln = 3, h = height_list, w=width_list, txt = 'OPUS Version: {}'.format(version))
        pdf.cell(ln = 3, h = height_list, w = width_list, txt = 'Operator: {}'.format(operator))


        pdf.set_xy(margin_def,baseline_start_height + 80)
        pdf.set_font('Arial', size = 9)
        pdf.cell(ln = 4, h = height_list, w = width_list, txt = 'Experiment filename:  {}'.format(experiment_filename))
        pdf.cell(ln = 4, h = height_list, w = width_list, txt = 'Method filename:  {}'.format(method_filename))
        pdf.cell(ln = 4, h = height_list, w = width_list, txt = 'Spectrum filename:  {}'.format(spectrum_filename))
        pdf.cell(ln = 4, h = height_list, w = width_list, txt = 'Spectrum pathname:  {}'.format(spectrum_pathname))

        # dict =  {
        #     "Product" : 'Ligustri lucidi fructus',
        #     "Gebindenummer" : 5325,
        #     "Charge" :  "17091212",
        #     "Ablaufdatum": '000000',
        #     "Gebinde": 'a'
        # }
    
        line_height = 0
        add = 7
        new_baseline = baseline_start_height + 120

        for i in productlabels_items:
            print(i)
            pdf.set_xy(margin_def ,baseline_start_height + 120 +line_height)
            pdf.cell(ln = 1, h = height_list, w = width_list, txt = '{}'.format(i[0]), align='l')
            pdf.set_xy(margin_def +60, baseline_start_height + 120 + line_height)
            pdf.cell(ln = 1, h = height_list, w = width_list, txt = '{}'.format(i[1]), align='l')
            line_height += 7
            new_baseline += add
            

        width_entry = (width_a4 -2*margin_def)/2
        print(width_entry)
        pdf.set_xy(margin_def,new_baseline + 15)
        pdf.set_font('Arial','B', size = 9)
        pdf.cell(ln = 2, h = height_list,  w = width_entry, txt = 'Classification', border = 1)
        pdf.set_font('Arial', size = 9)
        pdf.cell(ln = 2, h = height_list,  w = width_entry, txt = '{}'.format(identification), border = 1)


        pdf.set_xy(width_entry + margin_def,new_baseline + 15)
        pdf.set_font('Arial','B', size = 9)
        pdf.cell(ln = 2, h = height_list,  w = width_entry, txt = 'Result', border = 1)
        pdf.set_font('Arial', size = 9)
        pdf.cell(ln = 2, h = height_list,  w = width_entry, txt = '{}'.format(identification_result), border = 1)

        pdf.set_xy(margin_def, new_baseline + 30)
        pdf.set_font('Arial', size = 9)
        pdf.cell(ln = 1, h = height_list,  w = width_entry, txt = 'Comment: {}'.format(self.measurementwindow.commentedit.text()), align = 'l') 

        '''Draw Signature lines'''
        length_signature = 80
        gap_signature = 10
        pdf.line(margin_def,new_baseline + 60, width_entry +margin_def - gap_signature, new_baseline + 60)
        pdf.line(margin_def + width_entry + gap_signature, new_baseline + 60 , width_a4 - margin_def, new_baseline + 60)

        pdf.set_xy(margin_def/2 + (width_entry - margin_def - gap_signature)/2, new_baseline + 62)
        pdf.cell(ln = 1, h = height_list,  w = width_entry, txt = 'Signature (Operator)', align = 'l')
        pdf.set_xy(width_entry+margin_def + (width_entry - gap_signature - margin_def)/2, new_baseline + 62)
        pdf.cell(ln = 1, h = height_list,  w = width_entry, txt = 'Signature (Validation)', align = 'l')
        # # open the text file in read mode
        # f = open("txtfile.txt", "r")
        
        # # insert the texts in pdf
        # for x in f:
        #     pdf.cell(200, 10, txt = x, ln = 1, align = 'C')

        pdf.set_xy(margin_def,height_a4 - 2*margin_def - 1)
        # Select Arial italic 8
        pdf.set_font('Arial',size = 8)
        # Print centered page number
        pdf.cell(ln = 1, h = height_list,  w = width_entry, txt = 'Page %s' % pdf.page_no(), align = 'c')
        # pdf.cell(0, 10, 'Page %s' % pdf.page_no(), 0, 0, 'C')

        pdf.add_page()

        pdf.set_font("Arial", size = 9)
        pdf.set_xy(margin_def, baseline_start_height)
        pdf.set_line_width(0.0)

        pdf.set_right_margin(15)
        pdf.set_right_margin(15)

        f = open("analysis_report/Phytax_info.txt", "r")
        for x in f:
            #pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt='Phytax GmbH', border=0)
            pdf.cell(200, 4, txt = x, ln = 3, align = 'L')

        pdf.set_xy(0, baseline_start_height + 30)
        pdf.set_font("Arial",'B', size = 13 )
        pdf.cell(200, 10, "Spectra Plot", align = 'C')

        line_height = 0
        pdf.set_font('Arial', size = 9)
        for i in productlabels_items:
            print(i)
            pdf.set_xy(margin_def ,baseline_start_height + 50 +line_height)
            pdf.cell(ln = 1, h = height_list, w = width_list, txt = '{}'.format(i[0]), align='l')
            pdf.set_xy(margin_def +60, baseline_start_height + 50 + line_height)
            pdf.cell(ln = 1, h = height_list, w = width_list, txt = '{}'.format(i[1]), align='l')
            line_height += 7
            new_baseline += add
            
        path_image = r'analysis_report/plot_spectra.png'
        pdf.image(name = path_image,w = width_a4 - margin_def, h = 150, x = margin_def)
        pdf.set_xy(margin_def,height_a4 - 2*margin_def - 1)
        # Select Arial italic 8

        pdf.set_font('Arial',size = 8)
        # Print centered page number
        pdf.cell(ln = 1, h = height_list,  w = width_entry, txt = 'Page %s' % pdf.page_no(), align = 'c')

        settings = QSettings("Phytax", "Phydent")
        now = datetime.now()
        formated_data = now.strftime("%Y%m%d%H%M%S")
        path_report = Path(settings.value("report_path"))
        name_report = 'reportAnalysis{}'.format(formated_data)
        # save the pdf with name .pdf
        new_path = '{}\\{}.pdf'.format(path_report, name_report)
        new_path.replace('\\', '/')
        pdf.output(new_path)
        #pdf.output("report_of_analysis.pdf")   
        #os.system("report_of_analysis.pdf")
        subprocess.Popen([new_path], shell=True)
    
    def create_report(self):

        settings = QSettings("Phytax", "Phydent")
        # save FPDF() class into 
        # a variable pdf

        path_file = opusrequest("127.0.0.1", 80,"GET_SELECTED")[1]

        opus_path = os.path.basename(opusrequest("127.0.0.1", 80,"GET_OPUSPATH")[1])
        opus_version = opusrequest("127.0.0.1", 80, "GET_VERSION")[0]

        version = "{} ({})".format(opus_path, opus_version)
        # print(path_file)
        # print(path_file[1:])
        rewritten_path = ""
        for s in path_file[1:]:
            if s != '"':
                rewritten_path += s
            else:
                break
        
        path = Path(rewritten_path)
        print(rewritten_path)
        spectrum_pathname = path.parent.absolute()
        spectrum_filename = os.path.basename(path) 


        opusrequest("127.0.0.1", 80,"UNLOAD_FILE {}".format(path_file))
        opus_data = read_file(rewritten_path)

        opus_data_sample = opus_data['Sample']
        opus_data_instrument = opus_data['Instrument']
        opus_data_scrf = opus_data['ScRf Data Parameter']

        operator = opus_data_sample['CNM']
        experiment_filename = opus_data_sample['EXP']
        serial_number = opus_data_instrument['SRN'][:-1]
        spectrometer = r'Instruments\ALPHA\NTI\Alpha (Serial number {})'.format(serial_number)
        time_measurement = opus_data_scrf['TIM'][0:8]
        date_measurement = opus_data_scrf['DAT']
        date_time = date_measurement + ' ' + time_measurement

        spectrum_filename = spectrum_filename + ' ' + "({})".format(date_time)

        # print(version)
        # print(spectrum_pathname)
        # print(experiment_filename)
        # print(spectrum_filename)
        # print(spectrometer)

        '''OPUS METADATA'''
        #spectrometer = "Instruments"
        #version = 'Opus version 8.5'
        #operator = 'Peter Staub'
        #experiment_filename = 'test'
        method_filename = 'Phydent252452.snt'
        #spectrum_filename = 'Ligustri fructus 2235'
        #spectrum_pathname = r'C:\Users\Public\Documents\Bruker'

        '''Load the file back into OPUS'''
        # reformed_path = path.replace("\", r"\\")
        opusrequest("127.0.0.1", 80, "LOAD_FILE {}".format(path))

        identification = self.measurementwindow.classname.text()
        identification_result = self.measurementwindow.confidence.text()

        metadata_array = [spectrometer, version, operator, experiment_filename, method_filename, spectrum_filename, 
                            spectrum_pathname, identification, identification_result]

        

        dict_labels = {
            "productlabel1edit" : self.measurementwindow.productlabel1edit.text(),
            "productlabel2edit" : self.measurementwindow.productlabel2edit.text(),
            "productlabel3edit" : self.measurementwindow.productlabel3edit.text(),
            "productlabel4edit" : self.measurementwindow.productlabel4edit.text(),
            "productlabel5edit" : self.measurementwindow.productlabel5edit.text()
        }

        dict = {}
        labels = ["productlabel1", "productlabel2","productlabel3", "productlabel4", "productlabel5"]
        for i in labels:
            # print(i)
            # print(settings.value("{}check".format(i)))
            if settings.value("{}check".format(i)) == 'true':
                # print(settings.value(i))
                dict["{}".format(settings.value(i))] = dict_labels['{}edit'.format(i)]
        #if settings.value("produtlabel1check") == True:

        productlabels_items = dict.items()
   
        self.create_report_pdf(metadata_array, productlabels_items)


    def measurementstart(self):
        
        settings = QSettings("Phytax", "Phydent")
        path = settings.value("data_path")
        
         # Instantiate measurement class 

        productlabel1 = self.productlabel1edit.text()
        productlabel2 = self.productlabel2edit.text()
        productlabel3 = self.productlabel3edit.text()
        productlabel4 = self.productlabel4edit.text()
        productlabel5 = self.productlabel5edit.text()
        text_start_prompt = "[{}]: Messung gestartet".format(self.gettime())

        self.worker = OPUS.OPUS_measurement()

        self.worker.target_path = path

        self.measurementwindow = measurement(productlabel1, productlabel2, productlabel3, productlabel4, productlabel5,self.mainwindow_app)

        self.measurementwindow.backbutton.clicked.connect(self.go_back)
        self.measurementwindow.printbutton.clicked.connect(self.create_report)
        #new class
        #self.measurementwindow = measurement(productlabel1, productlabel2, productlabel3)

        
        #self.measurementwindow.logPrompt.setText("Messung gestartet...")
        self.measurementwindow.logPrompt.setStyleSheet("color : {};".format(self.label_color))
        self.measurementwindow.logPrompt.setText(text_start_prompt)
        self.measurementwindow.logPrompt.setReadOnly(True)
        self.measurementwindow.graphicsView.setBackground("w")
        #self.measurementwindow.graphicsView.plot(hour,temperature)
        
        self.measurementwindow.show()
        #self.popups.append(self.measurementwindow)
        self.mainwindow_app.hide()
        
        self.thread = QThread(self.measurementwindow)
        # Create worker object, Instantiate class
        

        #self.worker.target_path = path
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        #self.thread.started.connect(self.worker.opusrequest("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})"))
        #self.thread.started.connect(self.worker.opusrequest_fireandforget("127.0.0.1", 80, "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}})".format(path)))
        #self.worker.progress.connect(self.progress_measurement)
        self.worker.finished.connect(self.thread.quit)
        #self.worker.finished.connect(self.worker.deleteLater)
        #self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.r)
        self.thread.start()

        # self.thread.finished.connect(
        #     lambda: self.lastbackgroundmeasurementlabel.setText("Test")
        # )

        self.thread.finished.connect(
            self.updatelog
        )

    def readspectraldata(self):

        '''Should be the same in the Neural Network Training'''
        cutoff_threshold = '701.4029980023192'

        cwdir = os.getcwd()
        spectrum_data = pd.read_csv("{}/spectra_csv/spectra_pre.csv".format(cwdir))
        print(spectrum_data)
        x_values = spectrum_data.copy() 
        x_values = x_values.drop(['Filename',"Product","Dataset","Augmented"], inplace = True, axis = 1)

        x_points = []
        with open('{}/spectra_csv/x_points.txt'.format(cwdir), 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                x_points.append(currentPlace)
        x_points = [float(x) for x in x_points]
        #I believe the points are reversed
        #x_points.reverse()

        spectrum_data.drop("Filename", inplace = True, axis=1)
        spectrum_data.drop("Product", inplace = True, axis=1)
        spectrum_data.drop("Dataset", inplace = True, axis=1)
        spectrum_data.drop("Augmented", inplace = True, axis=1)

        '''Cutoff Data'''
        x_threshold = spectrum_data.columns.get_loc(cutoff_threshold)
        x_cutoff = spectrum_data.columns.get_loc('3994.45464922937')
        cutoff_spectrum_data = spectrum_data.iloc[:,x_cutoff:x_threshold]

        print(cutoff_spectrum_data)

        return spectrum_data, x_points, cutoff_spectrum_data

    def create_png_plot(self, x_point, y_point):
        plt.clf()
        plt.xlabel(r'Wavenumber [cm$^{-1}$]')
        plt.ylabel("Absorbance units")
        plt.plot(x_point,y_point, linewidth = 1, color = 'black')
        plt.gca().invert_xaxis()
        plt.savefig('analysis_report/plot_spectra.png', dpi=300)

    def plotspectra(self, spectrum_data, x_points):
        spectrum_data = np.array(spectrum_data)
        spectrum_data = spectrum_data[0].tolist()
        curve = self.measurementwindow.graphicsView.plot(x_points,spectrum_data)
        self.create_png_plot(x_points, spectrum_data)
        curve.getViewBox().invertX(True)

    def NNmodel(self, path):
        model_name = os.path.basename(path)
        model = ks.models.load_model(path)
        print(model.summary())
        currentwd = os.getcwd() 
        '''Define encoder/decoder'''
        path_encoder_file = '\{}\classes_{}.npy'.format(path, model_name)
        path_encoder_file = "%s%s"  % (currentwd, path_encoder_file)
        encoder = LabelEncoder()
        encoder_array = np.load(path_encoder_file, allow_pickle = True)
        encoder = encoder.fit(encoder_array)

        return model, encoder

    def class_prediction(self, x_test, model, encoder):
        '''Make prediction with trained model'''
        digits = 0
        y_prob = model.predict(x_test)
        y_prob.round(2)
        prediction_certainty = np.round(np.max(y_prob)*100, 2)
        '''Returns integer from encoder corresponding to a given class'''
        class_prediction=np.argmax(y_prob,axis=1)
        print(class_prediction)
        print(encoder.inverse_transform(class_prediction))
        encoder_output = encoder.inverse_transform(class_prediction)[0]
        #encoder_output = str(encoder.inverse_transform(class_prediction)[0], 'utf-8')
        for character in encoder_output:
            if character.isdigit():
                digits += 1
        encoder_output = encoder_output[:len(encoder_output) - digits-1]
        return encoder_output,  prediction_certainty
        
    def updatelog(self):
        currentwd = os.getcwd()
        print('arrived')
        text_log_finished = "[{}]: Messung abgeschlossen".format(self.gettime())

        #self.measurementwindow.logPrompt.append("Messung abgeschlossen")
        self.measurementwindow.logPrompt.append(text_log_finished)

        self.measurementwindow.logPrompt.append("[{}]: Vorverarbeitung des Spektrums".format(self.gettime()))
        np.set_printoptions(precision = 3, suppress = True)
        self.measurementwindow.printbutton.setEnabled(True)

        spectrum_data, x_points, cutoff_spectrum_data = self.readspectraldata()
        classification_data = cutoff_spectrum_data.copy()        
        self.plotspectra(spectrum_data, x_points)

        '''Select NN Model'''
        settings = QSettings("Phytax", "Phydent")
        chosen_model = settings.value("chosenNNmodel")
        print("Model used for Classification: {}".format(chosen_model))
        model, encoder = self.NNmodel('phydent_models/{}'.format(chosen_model))
            # this corresponds to a simple dense NN


        '''Scale the input data to be NN friendly'''
        xscaler = GlobalStandardScaler()
        classification_data = xscaler.fit_transform(classification_data)
        print("Input data NN: {}".format(classification_data))
        # '''Drop additional points initial points for classification'''
        # path_txtfile = r'\spectra_csv\x_points.txt'
        # txtfile = open("%s%s" % (currentwd,path_txtfile))
        # points_split = txtfile.read().splitlines()
        # for i in range(0,4):
        #     classification_data.drop(points_split[i], inplace = True, axis = 1, ignore_errors = True)
        # classification_data = classification_data.dropna(axis = 1)

        # print(classification_data)
        # print(np.shape(classification_data))

        '''Obtain information on the input shape of the model to determine whether the data needs to be reshaped or not'''
        layer_array = [layer.input_shape for layer in model.layers]

        length_input_dimension = len(layer_array[0])
        # Corresponds to a simple dense NN
        # if length_input_dimension == 2:
        #     # this corresponds to a simple dense NN
        if length_input_dimension == 3:
            classification_data = np.expand_dims(classification_data, axis=2)

        '''Obtain Prediction and prediction 'probability'''
        predicted_class = self.class_prediction(classification_data, model, encoder)
        predicted_probability = "{}%".format(np.round(predicted_class[1],1))
        self.measurementwindow.classname.setText(predicted_class[0])
        self.measurementwindow.confidence.setText(predicted_probability)

        # path_identification_image = '{}/Icons/negative.png'.format(currentwd)
        # pixmap = QPixmap(path_identification_image)
        # print(pixmap)
        # self.measurementwindow.identification_image.setPixmap(pixmap)

        '''Display red or green image'''
        if predicted_class[1] > 95:
            print("Prediction was positive")
            path_identification_image = '{}/Icons/positive.png'.format(currentwd)
            pixmap = QPixmap(path_identification_image)
            print(pixmap)
            self.measurementwindow.identification_image.setPixmap(pixmap)
            self.update()
            self.measurementwindow.update()
        else:
            print("Prediction was negative")
            path_identification_image = '{}/Icons/negative.png'.format(currentwd)
            pixmap = QPixmap(path_identification_image)
            print(pixmap)
            self.measurementwindow.identification_image.setPixmap(pixmap)
            self.update()
            self.measurementwindow.update()

    def gettime(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time
    
    def exitapp(self):

        #  self.measurementwindow.isVisible():
        # if measurement.class_instantiated == True:
        #     # dlg = QDialog(self)
        #     # dlg.setWindowTitle("Test")
        #     # dlg.label = QLabel
        #     # dlg.exec()
        #     dlg = QMessageBox(self)
        #     dlg.setWindowTitle("Test")
        #     dlg.setText("Eine Messung ist momentan am Laufen, wollen Sie die Anwendung wirklich schliessen")
        #     dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        #     #dlg.addButton("test")
        #     dlg.button
        #     dlg.setIcon(QMessageBox.Information)
        #     button = dlg.exec()

        #     if button == QMessageBox.Yes:
        #         print("Close Application")
        #         os.system("TASKKILL /F /IM opus.exe")
        #         sys.exit()
        #     else:
        #         print("Close Dialog")
        #         dlg.close()
        self.writeSettings()
        result = isinstance(self.thread, QThread)
        print("The background_measurement exists: {}".format(result))
        if self.background_measurement_thread == True:
            dlg = QMessageBox(self)
            dlg.setText("Eine Hintergrundmessung ist momentan am Laufen, wollen Sie die Anwendung wirklich schliessen")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            #dlg.addButton("test")
            dlg.button
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()

            if button == QMessageBox.Yes:
                print("Close Application")
                os.system("TASKKILL /F /IM opus.exe")
                sys.exit()
            else:
                print("Close Dialog")
                dlg.close()
        
        else:
            os.system("TASKKILL /F /IM opus.exe")
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
    #app.setStyle('Fusion')
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
