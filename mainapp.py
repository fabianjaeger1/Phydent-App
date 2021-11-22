import sys 
from PyQt5 import QtWidgets, uic
app = QtWidgets.QApplication(sys.argv) 
window = uic.loadUi("app.ui") 
window.show() 
app.exec_()