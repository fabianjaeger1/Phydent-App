# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 410)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LogoImage = QtWidgets.QLabel(self.centralwidget)
        self.LogoImage.setGeometry(QtCore.QRect(90, 10, 500, 70))
        self.LogoImage.setMinimumSize(QtCore.QSize(500, 70))
        self.LogoImage.setMaximumSize(QtCore.QSize(500, 70))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.LogoImage.setFont(font)
        self.LogoImage.setText("")
        self.LogoImage.setPixmap(QtGui.QPixmap("phydent-logo-2x.png"))
        self.LogoImage.setScaledContents(False)
        self.LogoImage.setObjectName("LogoImage")
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 90, 601, 211))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1, 25, -1)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(25)
        self.gridLayout.setObjectName("gridLayout")
        self.passlabel = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.passlabel.setFont(font)
        self.passlabel.setObjectName("passlabel")
        self.gridLayout.addWidget(self.passlabel, 2, 0, 1, 1)
        self.passinpu = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.passinpu.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.passinpu.setFont(font)
        self.passinpu.setObjectName("passinpu")
        self.gridLayout.addWidget(self.passinpu, 2, 1, 1, 1)
        self.userlabel = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.userlabel.setFont(font)
        self.userlabel.setObjectName("userlabel")
        self.gridLayout.addWidget(self.userlabel, 1, 0, 1, 1)
        self.userinput = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.userinput.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.userinput.setFont(font)
        self.userinput.setObjectName("userinput")
        self.gridLayout.addWidget(self.userinput, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(19, 330, 601, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.loginbutton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.loginbutton.setMinimumSize(QtCore.QSize(30, 30))
        self.loginbutton.setMaximumSize(QtCore.QSize(120, 40))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.loginbutton.setFont(font)
        self.loginbutton.setStyleSheet("color: rgb(0, 94, 135);")
        self.loginbutton.setObjectName("loginbutton")
        self.horizontalLayout_2.addWidget(self.loginbutton)
        self.exitbutton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exitbutton.setMinimumSize(QtCore.QSize(0, 40))
        self.exitbutton.setMaximumSize(QtCore.QSize(120, 40))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.exitbutton.setFont(font)
        self.exitbutton.setStyleSheet("color: rgb(0, 94, 135);")
        self.exitbutton.setObjectName("exitbutton")
        self.horizontalLayout_2.addWidget(self.exitbutton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.passlabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#698a93;\">Passwort:</span></p></body></html>"))
        self.userlabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#698a93;\">Benutzername:</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#005e87;\">OPUS Login Daten</span></p></body></html>"))
        self.loginbutton.setText(_translate("MainWindow", "Login"))
        self.exitbutton.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
