from PyQt5 import QtWidgets, QtGui, QtCore


class GenConfigWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)

    def get_config(self)->dict:
        return {}
