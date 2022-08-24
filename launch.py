#!/usr/bin/python3.8

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFileDialog, QGraphicsScene
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt


from MultiHex2.guis.main_gui import main_gui
from MultiHex2.tools import Clicker
from MultiHex2.clock import Time
from MultiHex2.generation.overland import fullsim
from MultiHex2.guis.savewarn import SaveWarnDialogGui
from MultiHex2.main_menu import MainMenuDialog
from MultiHex2.modules import ALL_MODULES
from MultiHex2.generation.map_gen_config import MapGenConfigDialog
from MultiHex2.tools.basic_tool import Basic_Tool

import os
import sys
import shutil
import json


if sys.platform=="linux":
    SAVEDIR = os.path.join(os.environ["HOME"], ".local", "MultiHex")
elif sys.platform=="darwin":
    raise NotImplementedError("You could probably swap error out for the linux SAVEDIR setting... I think the filesystems is similar?")
elif sys.platform=="win32":
    SAVEDIR = os.path.join(os.environ["AppData"], "MultiHex")
else:
    raise NotImplementedError("Unrecognized os {}".format(sys.platform))

if not os.path.exists(SAVEDIR):
    os.mkdir(SAVEDIR)

class WarnWidget(QtWidgets.QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ui = SaveWarnDialogGui()
        self.ui.setupUi(self)
        self.parent = parent


class main_window(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),"MultiHex2", 'assets','multihex_small_logo.svg')))

        # standard boiler-plate gui initialization
        # we instantiate the default GUI before anything else 
        self.ui = main_gui()
        self.ui.setupUi(self)

        self.scene = Clicker( self.ui.graphicsView, self )
        self.ui.events.configure(self.scene)
        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.ui.graphicsView.setScene( self.scene )
        self.ui.graphicsView.setMouseTracking(True)

        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.export_image.triggered.connect(self.export_image)


        config_name = ".config.json"
        self.config_filepath = os.path.join(SAVEDIR, config_name)
        if not os.path.exists(self.config_filepath):
            shutil.copyfile(os.path.join(os.path.dirname(__file__),"MultiHex2", "resources", "template_config.json"), self.config_filepath)
        
        self.module = None
        self.reload_config()

        self._loaded_module = False
        self._will_generate = False
        self.load_module(self.config["module"])
        self.select_tool("basic")
        self.open_menu()

        self.tileset = ""
        self.generator = None

        if self._will_generate:
            success = self.new()
            while not success:
                self.open_menu()
        


    def update_clock_gui(self,time:Time):
        self.ui.clock.set_time(time)

    def jump_to_time(self, time:Time):
        self.scene.skip_to_time(time)

    def reload_config(self):
        """
        Load in a config file. 

        If there's no module loaded yet, don't do anything yet! We're still in the setup phase

        Otherwise check if the module type has changed, and if so swap out the modules
        """
        f = open(self.config_filepath, 'rt')
        self.config = json.load(f)
        f.close()

        self.scene.set_primary_mouse(self.config["primary_mouse"]=="left")

        if self.module is not None:
            if self.config["module"]!=self.module.name:
                self.load_module(self.config["module"])

    def clear_tools(self):
        """
        clears otu the tools, used when we load new modules in 
        """
        self.scene._alltools = {}
        self.add_tool("basic", Basic_Tool) 
        if self._loaded_module:
            self.select_tool("basic")

    def load_module(self, module_name:str):
        """
        Clear all the buttons, tell the scene to delete all its tools

        Then, add in all the relevant tools 
        """
        if self.module is not None:
            if self.module.name==module_name: # the module is already loaded, don't waste time
                return

        self.ui.clear_buttons()
        self.clear_tools()

        
        self.module = ALL_MODULES[module_name]()
        self.scene.module = module_name
        self.scene.update_with_module()

        self.scene.tileset = self.module.tileset
        all_tools = self.module.tools
        for key in all_tools:
            self.add_tool(key, all_tools[key])
        self.generator = self.module.generator_function
        print("Loaded Module '{}'".format(self.module.name))
        self._loaded_module = True

    def open_menu(self):
        accepted = False

        while not accepted:
            dialog = MainMenuDialog(self)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

            accepted = dialog.Accepted

    def export_image(self):
        temp= QFileDialog.getSaveFileName(None, 'Exoport Image', SAVEDIR, 'PNGs (*.png)')[0]
        if temp is None:
            return
        elif temp=='':
            return
        
        #self.main_map.dimensions
        size   = QtCore.QSize(self.scene.dimensions[0], self.scene.dimensions[1])
        image  = QtGui.QImage(size,QtGui.QImage.Format_ARGB32_Premultiplied)
        painter= QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(temp)

    def new(self):
        """
        Returns True if this successfully starts making a new map, otherwise returns False
        """
        if not self._loaded_module:
            self._will_generate = True
            return True
        else:
            dialog = MapGenConfigDialog(self, self.module.generation_config)
            #dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()
            dialog.deleteLater()

            if dialog.Accepted:
                use_configs = dialog.get_config()
                seed = dialog.get_seed()
                self.generator(self.scene, config=use_configs, seed=seed) 
                self.ui.clock.set_time(self.scene.clock.time)
                self.ui.events.update()
                return True
            else:
                return False

    def save(self):
        self.scene.reset_save()

        if self.scene.file_name=="":
            self.saveAs()
        else:
            self.scene.save(self.scene.file_name)    

    def saveAs(self):
        pathto = QFileDialog.getSaveFileName(None, 'Save As',SAVEDIR, 'Json (*.json)')[0]
        if pathto is not None:
            if pathto!="":
                self.scene.save(pathto)
                self.scene.reset_save()

    def quit(self):
        if self.scene.unsaved:
            self.dialog = WarnWidget(parent=self)
            self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.dialog.exec_()

        sys.exit()

    def load(self)->str:
        pathto = QFileDialog.getOpenFileName(None, 'Save As',SAVEDIR, 'Json (*.json)')[0]
        if pathto is not None:
            if pathto!="":
                self.scene.load( pathto)
                self.scene.reset_save()

        if self.module is not None:
            if self.scene.module == self.module.name:
                return pathto

        self.load_module(self.module.name)
        return pathto

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key()==Qt.Key_Escape:
            self.select_tool("basic")

    def add_tool(self,tool_name:str, tool:Basic_Tool):

        self.ui.add_button(tool_name, tool.buttonIcon(), tool.altText(), tool.tool_layer() )
        def tempfunc():
            return self.select_tool(tool_name)
        
        value = tool.tool_layer().value
        if value==0 or value==1:
            self.ui.buttons[tool_name].clicked.connect(tempfunc)
        elif value==2:
            self.ui.second_buttons[tool_name].clicked.connect(tempfunc)
        elif value==4:
            self.ui.map_use_buttons[tool_name].clicked.connect(tempfunc)
        else:
            raise NotImplementedError("Not layer {}".format(tool.tool_layer()))

        self.scene.add_tool(tool_name, tool)

    def select_tool(self, tool_name:str):
        self.scene.select_tool(tool_name)
        
        if self.ui.toolwidget is not None:
            self.ui.toolPane.removeWidget(self.ui.toolwidget)
            self.ui.toolwidget.deleteLater()
            self.ui.toolwidget = None
        self.ui.toolwidget = self.scene.tool.widget()(self.ui.centralwidget, self.scene.tool, self.module.tileset, self.module.text_source)
        self.ui.toolPane.addWidget(self.ui.toolwidget)
        self.ui.toolPane.update()
        

app = QApplication(sys.argv)
app_instance = main_window()

if __name__=="__main__":
    # make sure the base saves folder exists 
    app_instance.show()
    sys.exit(app.exec_())
