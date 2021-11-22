# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logindialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(599, 380)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(599, 380))
        Dialog.setMaximumSize(QtCore.QSize(599, 380))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(30, 15, 30, 10)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LogoImage = QtWidgets.QLabel(Dialog)
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
        self.verticalLayout.addWidget(self.LogoImage)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1, 25, -1)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(25)
        self.gridLayout.setObjectName("gridLayout")
        self.passlabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.passlabel.setFont(font)
        self.passlabel.setObjectName("passlabel")
        self.gridLayout.addWidget(self.passlabel, 1, 0, 1, 1)
        self.userlabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.userlabel.setFont(font)
        self.userlabel.setObjectName("userlabel")
        self.gridLayout.addWidget(self.userlabel, 0, 0, 1, 1)
        self.userinput = QtWidgets.QLineEdit(Dialog)
        self.userinput.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.userinput.setFont(font)
        self.userinput.setObjectName("userinput")
        self.gridLayout.addWidget(self.userinput, 0, 1, 1, 1)
        self.passinpu = QtWidgets.QLineEdit(Dialog)
        self.passinpu.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.passinpu.setFont(font)
        self.passinpu.setObjectName("passinpu")
        self.gridLayout.addWidget(self.passinpu, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginbutton = QtWidgets.QPushButton(Dialog)
        self.loginbutton.setMinimumSize(QtCore.QSize(30, 30))
        self.loginbutton.setMaximumSize(QtCore.QSize(120, 40))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.loginbutton.setFont(font)
        self.loginbutton.setObjectName("loginbutton")
        self.horizontalLayout.addWidget(self.loginbutton)
        self.exitbutton = QtWidgets.QPushButton(Dialog)
        self.exitbutton.setMinimumSize(QtCore.QSize(0, 40))
        self.exitbutton.setMaximumSize(QtCore.QSize(120, 40))
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(12)
        self.exitbutton.setFont(font)
        self.exitbutton.setObjectName("exitbutton")
        self.horizontalLayout.addWidget(self.exitbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.label.setText(_translate("Dialog", "OPUS Login Daten"))
        self.passlabel.setText(_translate("Dialog", "Passwort:"))
        self.userlabel.setText(_translate("Dialog", "Benutzername:"))
        self.loginbutton.setText(_translate("Dialog", "Login"))
        self.exitbutton.setText(_translate("Dialog", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
