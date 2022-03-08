from PyQt5 import QtCore, QtGui, QtWidgets

import os

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
        self.buttons = {}
        self.toolwidget = None
        self.toolPane.addLayout(self.buttonGrid)
        self.toolPane.addItem(spacerItem)


        self.horizontalLayout.addLayout(self.toolPane)

        # define the screen
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget) # <--- this is the screen
        self.graphicsView.setObjectName("graphicsView") 
        self.horizontalLayout.addWidget(self.graphicsView)


        # and nest it! 
        MainWindow.setCentralWidget(self.centralwidget)

        # self.toolBox.setItemText(self.toolBox.indexOf(self.paneItem), _translate("MainWindow", "Detailer"))

        # and then the menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1109, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEditor = QtWidgets.QMenu(self.menubar)
        self.menuEditor.setObjectName("menuEditor")
        
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

        self.actionTerrainEditor = QtWidgets.QAction(MainWindow)
        self.actionTerrainEditor.setCheckable(True)
        self.actionTerrainEditor.setObjectName("actionTerrainEditor")
        self.actionCivEditor = QtWidgets.QAction(MainWindow)
        self.actionCivEditor.setCheckable(True)
        self.actionCivEditor.setObjectName("actionCivEditor")
        self.actionMapUse = QtWidgets.QAction(MainWindow)
        self.actionMapUse.setCheckable(True)
        self.actionMapUse.setObjectName("actionMapUse")
        
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.export_image)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        self.menuEditor.addAction(self.actionTerrainEditor)
        self.menuEditor.addAction(self.actionCivEditor)
        self.menuEditor.addAction(self.actionMapUse)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.setTitle(QtCore.QCoreApplication.translate("MainWinbdow","File"))
        self.actionNew.setText(QtCore.QCoreApplication.translate("MainWindow", "New"))
        self.actionOpen.setText(QtCore.QCoreApplication.translate("MainWindow", "Open"))
        self.actionSave.setText(QtCore.QCoreApplication.translate("MainWindow", "Save"))
        self.actionSave_As.setText(QtCore.QCoreApplication.translate("MainWindow", "Save As"))
        self.export_image.setText(QtCore.QCoreApplication.translate("MainWindow","Export Image"))
        self.actionQuit.setText(QtCore.QCoreApplication.translate("MainWindow", "Quit"))

        self.menubar.addAction(self.menuEditor.menuAction())
        self.menuEditor.setTitle(QtCore.QCoreApplication.translate("MainWinbdow","Editor"))
        self.actionTerrainEditor.setText(QtCore.QCoreApplication.translate("MainWinbdow","Terrain Editor"))
        self.actionCivEditor.setText(QtCore.QCoreApplication.translate("MainWindow","Civilization Editor"))
        self.actionMapUse.setText(QtCore.QCoreApplication.translate("MainWindow", "Map Use Mode"))



        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def add_button(self, name:str, button:QtGui.QPixmap, alt_text=""):
        new_button = QtWidgets.QPushButton(self.centralwidget)
        new_button.setObjectName(name)
        new_button.setToolTip(alt_text)
        new_button.setIcon(QtGui.QIcon(button))
        new_button.setIconSize(QtCore.QSize(48,48))
        new_button.setFixedWidth(64)
        new_button.setFixedHeight(64)
        #new_button.setText(name)
        buttons = len(self.buttons.keys())
        is_odd = buttons%2==1
        column = 1 if is_odd else 0
        row = int(buttons/2)

        self.buttons[name] = new_button
        self.buttonGrid.addWidget(new_button, row, column)
        
