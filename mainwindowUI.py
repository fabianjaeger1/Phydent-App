# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Messungen(object):
    def setupUi(self, Messungen):
        Messungen.setObjectName("Messungen")
        Messungen.resize(832, 653)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Messungen.sizePolicy().hasHeightForWidth())
        Messungen.setSizePolicy(sizePolicy)
        Messungen.setMaximumSize(QtCore.QSize(16777215, 16777195))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        Messungen.setFont(font)
        Messungen.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(Messungen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(40, 40, 40, 40)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Logo = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Logo.sizePolicy().hasHeightForWidth())
        self.Logo.setSizePolicy(sizePolicy)
        self.Logo.setMaximumSize(QtCore.QSize(300, 120000))
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("phydent-logo-2x.png"))
        self.Logo.setScaledContents(False)
        self.Logo.setObjectName("Logo")
        self.verticalLayout.addWidget(self.Logo)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.backgroundmeasurementsection = QtWidgets.QHBoxLayout()
        self.backgroundmeasurementsection.setObjectName("backgroundmeasurementsection")
        self.backgroundbutton = QtWidgets.QPushButton(self.centralwidget)
        self.backgroundbutton.setMinimumSize(QtCore.QSize(300, 50))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.backgroundbutton.setFont(font)
        self.backgroundbutton.setAutoFillBackground(False)
        self.backgroundbutton.setStyleSheet("color: rgb(0, 71, 102);")
        self.backgroundbutton.setObjectName("backgroundbutton")
        self.backgroundmeasurementsection.addWidget(self.backgroundbutton)
        self.lastbackgroundmeasurementlabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        self.lastbackgroundmeasurementlabel.setFont(font)
        self.lastbackgroundmeasurementlabel.setStyleSheet("color: rgb(34, 34, 34);")
        self.lastbackgroundmeasurementlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lastbackgroundmeasurementlabel.setObjectName("lastbackgroundmeasurementlabel")
        self.backgroundmeasurementsection.addWidget(self.lastbackgroundmeasurementlabel)
        self.verticalLayout.addLayout(self.backgroundmeasurementsection)
        self.productinformationsection = QtWidgets.QVBoxLayout()
        self.productinformationsection.setObjectName("productinformationsection")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.productinformationsection.addItem(spacerItem1)
        self.productinformationlabel = QtWidgets.QLabel(self.centralwidget)
        self.productinformationlabel.setMinimumSize(QtCore.QSize(0, 40))
        self.productinformationlabel.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.productinformationlabel.setFont(font)
        self.productinformationlabel.setObjectName("productinformationlabel")
        self.productinformationsection.addWidget(self.productinformationlabel)
        self.productinformationgrid = QtWidgets.QGridLayout()
        self.productinformationgrid.setVerticalSpacing(20)
        self.productinformationgrid.setObjectName("productinformationgrid")
        self.productlabel2edit = QtWidgets.QLineEdit(self.centralwidget)
        self.productlabel2edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel2edit.setFont(font)
        self.productlabel2edit.setText("")
        self.productlabel2edit.setObjectName("productlabel2edit")
        self.productinformationgrid.addWidget(self.productlabel2edit, 1, 1, 1, 1)
        self.productlabel3 = QtWidgets.QLabel(self.centralwidget)
        self.productlabel3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel3.setFont(font)
        self.productlabel3.setObjectName("productlabel3")
        self.productinformationgrid.addWidget(self.productlabel3, 2, 0, 1, 1)
        self.productlabel1 = QtWidgets.QLabel(self.centralwidget)
        self.productlabel1.setMinimumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel1.setFont(font)
        self.productlabel1.setObjectName("productlabel1")
        self.productinformationgrid.addWidget(self.productlabel1, 0, 0, 1, 1)
        self.productlabel4 = QtWidgets.QLabel(self.centralwidget)
        self.productlabel4.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel4.setFont(font)
        self.productlabel4.setObjectName("productlabel4")
        self.productinformationgrid.addWidget(self.productlabel4, 3, 0, 1, 1)
        self.productlabel4edit = QtWidgets.QLineEdit(self.centralwidget)
        self.productlabel4edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel4edit.setFont(font)
        self.productlabel4edit.setText("")
        self.productlabel4edit.setObjectName("productlabel4edit")
        self.productinformationgrid.addWidget(self.productlabel4edit, 3, 1, 1, 1)
        self.productlabel1edit = QtWidgets.QLineEdit(self.centralwidget)
        self.productlabel1edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel1edit.setFont(font)
        self.productlabel1edit.setText("")
        self.productlabel1edit.setObjectName("productlabel1edit")
        self.productinformationgrid.addWidget(self.productlabel1edit, 0, 1, 1, 1)
        self.productlabel2 = QtWidgets.QLabel(self.centralwidget)
        self.productlabel2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel2.setFont(font)
        self.productlabel2.setObjectName("productlabel2")
        self.productinformationgrid.addWidget(self.productlabel2, 1, 0, 1, 1)
        self.productlabel3edit = QtWidgets.QLineEdit(self.centralwidget)
        self.productlabel3edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel3edit.setFont(font)
        self.productlabel3edit.setText("")
        self.productlabel3edit.setObjectName("productlabel3edit")
        self.productinformationgrid.addWidget(self.productlabel3edit, 2, 1, 1, 1)
        self.productlabel5 = QtWidgets.QLabel(self.centralwidget)
        self.productlabel5.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel5.setFont(font)
        self.productlabel5.setObjectName("productlabel5")
        self.productinformationgrid.addWidget(self.productlabel5, 4, 0, 1, 1)
        self.productlabel5edit = QtWidgets.QLineEdit(self.centralwidget)
        self.productlabel5edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.productlabel5edit.setFont(font)
        self.productlabel5edit.setText("")
        self.productlabel5edit.setObjectName("productlabel5edit")
        self.productinformationgrid.addWidget(self.productlabel5edit, 4, 1, 1, 1)
        self.productinformationsection.addLayout(self.productinformationgrid)
        self.verticalLayout.addLayout(self.productinformationsection)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startmeasurementbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startmeasurementbutton.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.startmeasurementbutton.setFont(font)
        self.startmeasurementbutton.setStyleSheet("color: rgb(0, 71, 102);")
        self.startmeasurementbutton.setObjectName("startmeasurementbutton")
        self.horizontalLayout.addWidget(self.startmeasurementbutton)
        self.startmeasurementbutton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.startmeasurementbutton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.startmeasurementbutton_2.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.startmeasurementbutton_2.setFont(font)
        self.startmeasurementbutton_2.setStyleSheet("color: rgb(0, 71, 102);")
        self.startmeasurementbutton_2.setObjectName("startmeasurementbutton_2")
        self.horizontalLayout.addWidget(self.startmeasurementbutton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        Messungen.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(Messungen)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.toolBar.setFont(font)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        Messungen.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAbout = QtWidgets.QAction(Messungen)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icons/info_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")
        self.actionEinstellungen = QtWidgets.QAction(Messungen)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icons/gear_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEinstellungen.setIcon(icon1)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(11)
        self.actionEinstellungen.setFont(font)
        self.actionEinstellungen.setObjectName("actionEinstellungen")
        self.toolBar.addAction(self.actionEinstellungen)
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(Messungen)
        QtCore.QMetaObject.connectSlotsByName(Messungen)
        Messungen.setTabOrder(self.backgroundbutton, self.productlabel1edit)
        Messungen.setTabOrder(self.productlabel1edit, self.productlabel2edit)
        Messungen.setTabOrder(self.productlabel2edit, self.productlabel3edit)
        Messungen.setTabOrder(self.productlabel3edit, self.productlabel4edit)
        Messungen.setTabOrder(self.productlabel4edit, self.productlabel5edit)
        Messungen.setTabOrder(self.productlabel5edit, self.startmeasurementbutton)
        Messungen.setTabOrder(self.startmeasurementbutton, self.startmeasurementbutton_2)

    def retranslateUi(self, Messungen):
        _translate = QtCore.QCoreApplication.translate
        Messungen.setWindowTitle(_translate("Messungen", "Phydent"))
        self.backgroundbutton.setText(_translate("Messungen", "Hintergrund messen"))
        self.lastbackgroundmeasurementlabel.setText(_translate("Messungen", "Letze Hintergrund Messung: 12.10.2021 09:31"))
        self.productinformationlabel.setText(_translate("Messungen", "<html><head/><body><p><span style=\" color:#004766;\">Produktinformation</span></p></body></html>"))
        self.productlabel3.setText(_translate("Messungen", "<html><head/><body><p><span style=\" color:#222222;\">Charge</span></p></body></html>"))
        self.productlabel1.setText(_translate("Messungen", "<html><head/><body><p><span style=\" color:#222222;\">Produktname</span></p></body></html>"))
        self.productlabel4.setText(_translate("Messungen", "<html><head/><body><p><span style=\" color:#222222;\">Ablaufdatum</span></p></body></html>"))
        self.productlabel2.setText(_translate("Messungen", "<html><head/><body><p><span style=\" color:#222222;\">Produktnumber</span></p></body></html>"))
        self.productlabel5.setText(_translate("Messungen", "<html><head/><body><p><span style=\" color:#222222;\">Gebinde</span></p></body></html>"))
        self.startmeasurementbutton.setText(_translate("Messungen", "Messung starten"))
        self.startmeasurementbutton_2.setText(_translate("Messungen", "Schliessen"))
        self.toolBar.setWindowTitle(_translate("Messungen", "toolBar"))
        self.actionAbout.setText(_translate("Messungen", "About"))
        self.actionEinstellungen.setText(_translate("Messungen", "Einstellungen"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Messungen = QtWidgets.QMainWindow()
    ui = Ui_Messungen()
    ui.setupUi(Messungen)
    Messungen.show()
    sys.exit(app.exec_())
