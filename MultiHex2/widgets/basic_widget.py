from PyQt5 import QtWidgets, QtGui

class ToolWidget(QtWidgets.QWidget):
    def __init__(self, parent, tool, tileset, text_source):
        QtWidgets.QWidget.__init__(self, parent)
        self._tool = tool

        self._tool.link_to_widget(self)
        self.tileset = tileset
        self.text_source = text_source
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)
        self.new_color = QtGui.QColor(0,0,0)
    
    @property
    def tool(self):
        return self._tool