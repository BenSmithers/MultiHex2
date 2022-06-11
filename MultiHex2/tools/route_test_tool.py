from MultiHex2.tools.basic_tool import Basic_Tool
from MultiHex2.core import HexID
from MultiHex2.core import screen_to_hex
import os 

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from MultiHex2.actions.baseactions import NullAction
from MultiHex2.core.coordinates import hex_to_screen

from MultiHex2.tools.basic_tool import ToolLayer

"""
Tools make actions 
"""

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

class RouteTester(Basic_Tool):
    def __init__(self, parent):
        Basic_Tool.__init__(self, parent)
        self.highlight = False

        self._start = None
        self._end = None

        self._drawing = None
        self.set_state(0)

    @classmethod
    def altText(cls):
        return "Route Tester Tool"

    def drawpath(self, start:HexID, end:HexID):
        if self._drawing is not None:
            self.parent.removeItem(self._drawing)
            self._drawing=None
        route = self.parent.get_route_a_star(start, end, True)
        positions = [hex_to_screen(id) for id in route]

        path = QtGui.QPainterPath()
        path.addPolygon(QtGui.QPolygonF(positions))


        
        self.parent._pen.setStyle(2)
        self.parent._pen.setWidth(5)
        self.parent._pen.setColor(QtGui.QColor(245,245,255))
        self.parent._brush.setStyle(0)
        self._drawing = self.parent.addPath(path,self.parent._pen, self.parent._brush)
        self._drawing.setZValue(120)
        self.parent.update()

    def mouse_moved(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        if self.state==1:
            loc = event.scenePos()
            here = screen_to_hex(loc)
            if self._end is None:
                if here!=self._start:
                    self.drawpath(self._start, here)
                    
                self._end = here
            elif self._end!=here:
                self.drawpath(self._start, here)
                self._end = here
                    

        return NullAction()

    def deselect(self):
        self.set_state(0)
        self._start=None

    def primary_mouse_released(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        print("Mouse release, state {}".format(self.state))
        if self.state==0:
            loc = event.scenePos()
            self._start = screen_to_hex(loc)
            self.set_state(1)
            print("set to state {}".format(self._state))

        if self.state==100000:
            self._start = None
            self.set_state(0)
            print("set state {}".format(self._state))

        return NullAction()
