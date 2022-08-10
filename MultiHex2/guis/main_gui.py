from PyQt5 import QtCore, QtGui, QtWidgets

import os
from MultiHex2.clock import MultiHexCalendar
from MultiHex2.clock import Time
from MultiHex2.actions.eventWidget import EventWidget
from MultiHex2.core.core import ToolLayer

"""
This file defines the gui for the MainWindow's structure
"""

class main_gui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "MultiHex"))

        # define the primary areas on the GUI
        #    the tool pane
        #    the screen

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # the tool pane! Icons should be added to this (by default it's empty)
        self.toolPane = QtWidgets.QVBoxLayout()
        self.toolPane.setObjectName("toolPane")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.buttonGrid = QtWidgets.QGridLayout()
        self.buttonGrid.setObjectName("buttonGrid")

        # line 
        self.firstLine = QtWidgets.QFrame(self.centralwidget)
        self.firstLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.firstLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.firstLine.setObjectName("firstLine")

        self.secondline = QtWidgets.QFrame(self.centralwidget)
        self.secondline.setFrameShape(QtWidgets.QFrame.HLine)
        self.secondline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.secondline.setObjectName("secondline")

        self.civButtonGrid = QtWidgets.QGridLayout()
        self.civButtonGrid.setObjectName("civButtonGrid")

        self.mapUseButtonGrid =  QtWidgets.QGridLayout()
        self.mapUseButtonGrid.setObjectName("mapUseButtonGrid")

        #ToolLayer
        self.buttons = {}
        self.second_buttons = {} # civ layer button
        self.map_use_buttons = {} # map use layer
        self.toolwidget = None
        self.toolPane.addLayout(self.buttonGrid)
        self.toolPane.addWidget(self.firstLine)
        self.toolPane.addLayout(self.civButtonGrid)
        self.toolPane.addWidget(self.secondline)
        self.toolPane.addLayout(self.mapUseButtonGrid)


        self.toolPane.addItem(spacerItem)
        

        self.horizontalLayout.addLayout(self.toolPane)

        # define the screen
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget) # <--- this is the screen
        self.graphicsView.setObjectName("graphicsView") 
        self.horizontalLayout.addWidget(self.graphicsView)
        

        self.clockPane = QtWidgets.QVBoxLayout()
        self.clockPane.setObjectName("clockPane")
        self.clock = MultiHexCalendar(self.centralwidget, Time())
        self.clockPane.addWidget(self.clock)

        self.events = EventWidget(self.centralwidget, None)
        self.clockPane.addWidget(self.events)

        secondSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.clockPane.addItem(secondSpacerItem)
        self.horizontalLayout.addLayout(self.clockPane)
        

        # and nest it! 
        MainWindow.setCentralWidget(self.centralwidget)

        # self.toolBox.setItemText(self.toolBox.indexOf(self.paneItem), _translate("MainWindow", "Detailer"))

        # and then the menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1109, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.export_image = QtWidgets.QAction(MainWindow)
        self.export_image.setObjectName("export_image")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.export_image)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)


        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.setTitle(QtCore.QCoreApplication.translate("MainWinbdow","File"))
        self.actionNew.setText(QtCore.QCoreApplication.translate("MainWindow", "New"))
        self.actionOpen.setText(QtCore.QCoreApplication.translate("MainWindow", "Open"))
        self.actionSave.setText(QtCore.QCoreApplication.translate("MainWindow", "Save"))
        self.actionSave_As.setText(QtCore.QCoreApplication.translate("MainWindow", "Save As"))
        self.export_image.setText(QtCore.QCoreApplication.translate("MainWindow","Export Image"))
        self.actionQuit.setText(QtCore.QCoreApplication.translate("MainWindow", "Quit"))

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def clear_buttons(self):
        for button_key in self.buttons.keys():
            self.buttonGrid.removeWidget(self.buttons[button_key])
            self.buttons[button_key].deleteLater()
        for button_key in self.second_buttons.keys():
            self.civButtonGrid.removeWidget(self.second_buttons[button_key])
            self.second_buttons[button_key].deleteLater()
        for button_key in self.map_use_buttons.keys():
            self.mapUseButtonGrid.removeWidget(self.map_use_buttons[button_key])
            self.map_use_buttons[button_key].deleteLater()

        self.buttons = {}
        self.second_buttons = {}
        self.map_use_buttons = {}

    def add_button(self, name:str, button:QtGui.QPixmap, alt_text="", layer=ToolLayer.null):
        new_button = QtWidgets.QPushButton(self.centralwidget)
        new_button.setObjectName(name)
        new_button.setToolTip(alt_text)
        new_button.setIcon(QtGui.QIcon(button))
        new_button.setIconSize(QtCore.QSize(48,48))
        new_button.setFixedWidth(64)
        new_button.setFixedHeight(64)
        layer_val = layer.value

        if layer_val==2:
            buttons =len(self.second_buttons.keys())
        elif layer_val==0 or layer_val==1:

            #new_button.setText(name)
            buttons = len(self.buttons.keys())
        elif layer_val==4:
            buttons = len(self.map_use_buttons.keys())
        else:
            print("Layer {}".format(layer))
            print(ToolLayer.terrain)
            print(ToolLayer.terrain==layer)
            raise NotImplementedError("Unimplemented layer {}".format(layer))

        is_odd = (buttons%2==1)
        column = 1 if is_odd else 0
        row = int(buttons/2)

        if layer_val==2:
            self.second_buttons[name] = new_button
            self.civButtonGrid.addWidget(new_button, row, column)
        elif layer_val==4:
            self.map_use_buttons[name] = new_button
            self.mapUseButtonGrid.addWidget(new_button, row, column)
        elif layer_val==0 or layer_val==1:
            self.buttons[name] = new_button
            self.buttonGrid.addWidget(new_button, row, column)
        
