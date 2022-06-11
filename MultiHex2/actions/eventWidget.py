import typing
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget

from MultiHex2.clock import Time, days_in_week
from MultiHex2.core.utils import get_cardinal

class TimeTableEntry(QtWidgets.QTableWidgetItem):
    def __init__(self, time_:Time):
        short_form = "{}/{}/{}".format(time_.month+1, time_.day+1, time_.year+1)

        QtWidgets.QTableWidgetItem.__init__(self, short_form)

        self.time = time_


class EventWidgetGui:
    def setupUi(self, Form):
        Form.setObjectName("Form")


        self.evt_formLayout = QtWidgets.QFormLayout(Form)
        self.evt_formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.evt_formLayout.setObjectName("evt_formLayout")

        self.evt_obj_name_lbl = QtWidgets.QLabel(Form)
        self.evt_obj_name_lbl.setObjectName("evt_obj_name_lbl")
        self.evt_obj_name_lbl.setText("Looking at: ")
        self.evt_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.evt_obj_name_lbl)
        self.evt_obj_name_disp = QtWidgets.QLabel(Form)
        self.evt_obj_name_disp.setObjectName("evt_obj_name_disp")
        self.evt_obj_name_disp.setText("${Object_Name}")
        self.evt_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.evt_obj_name_disp)
        self.evt_lat_lbl = QtWidgets.QLabel(Form)
        self.evt_lat_lbl.setObjectName("evt_lat_lbl")
        self.evt_lat_lbl.setText("Latitude: ")
        self.evt_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.evt_lat_lbl)
        self.evt_lat_disp = QtWidgets.QLabel(Form)
        self.evt_lat_disp.setObjectName("evt_lat_disp")
        self.evt_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.evt_lat_disp)
        self.evt_lon_lbl = QtWidgets.QLabel(Form)
        self.evt_lon_lbl.setObjectName("evt_lon_lbl")
        self.evt_lon_lbl.setText("Longitude: ")
        self.evt_formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.evt_lon_lbl)
        self.evt_lon_disp = QtWidgets.QLabel(Form)
        self.evt_lon_disp.setObjectName("evt_lat_disp")
        self.evt_formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.evt_lon_disp)
        self.evt_date_disp = QtWidgets.QLabel(Form)
        self.evt_date_disp.setObjectName("evt_date_disp")
        self.evt_date_disp.setText("10 August 2020, 8:43 PM")

        self.local_date_disp = QtWidgets.QLabel(Form)
        self.local_date_disp.setObjectName("local_date_disp")
        self.local_date_disp.setText("10 August 2020, 8:43 PM")
        self.evt_formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.evt_date_disp)
        self.evt_formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.local_date_disp)

        self.evt_next_evt_layout = QtWidgets.QHBoxLayout()
        self.evt_next_evt_layout.setObjectName("evt_next_evt_layout")
        self.evt_next_evt_button = QtWidgets.QPushButton(Form)
        self.evt_next_evt_button.setObjectName("evt_next_evt_button")
        self.evt_next_evt_button.setText("Next Event")
        self.evt_next_evt_layout.addWidget(self.evt_next_evt_button)
        self.evt_next_sun_button = QtWidgets.QPushButton(Form)
        self.evt_next_sun_button.setObjectName("evt_next_sun_button")
        self.evt_next_sun_button.setText("Next Suntime")
        self.evt_next_evt_layout.addWidget(self.evt_next_sun_button)
        self.evt_next_some_button = QtWidgets.QPushButton(Form)
        self.evt_next_some_button.setObjectName("evt_next_some_button")
        self.evt_next_some_button.setText("Something")
        self.evt_next_evt_layout.addWidget(self.evt_next_some_button)
        self.evt_formLayout.setLayout(6, QtWidgets.QFormLayout.SpanningRole, self.evt_next_evt_layout)
        self.evt_scroll_area = QtWidgets.QScrollArea()
        self.evt_scroll_area.setObjectName("evt_scroll_area")
        self.evt_formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.evt_scroll_area)
        self.evt_scroll_layout = QtWidgets.QVBoxLayout()
        self.evt_scroll_layout.setObjectName("evt_scroll_layout")
        self.evt_evt_table = QtWidgets.QTableWidget(Form)
        self.evt_evt_table.setColumnCount(2)
        self.evt_evt_table.setVerticalHeaderLabels(["Date","Description"])
        self.evt_evt_table.setSortingEnabled(True)
        self.evt_evt_table.setEnabled(False)

        self.evt_evt_table.horizontalHeader().setStretchLastSection(True)
        self.evt_evt_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.evt_scroll_layout.addWidget(self.evt_evt_table)
        self.evt_scroll_area.setLayout(self.evt_scroll_layout)
        self.evt_skip_layout = QtWidgets.QHBoxLayout()
        self.evt_skip_layout.setObjectName("evt_skip_layout")
        self.evt_skip_button = QtWidgets.QPushButton(Form)
        self.evt_skip_button.setObjectName("evt_skip_button")
        self.evt_skip_button.setText("Skip")
        self.evt_skip_layout.addWidget(self.evt_skip_button)
        self.evt_skip_number_spin = QtWidgets.QSpinBox(Form)
        self.evt_skip_number_spin.setObjectName("evt_skip_number_spin")
        self.evt_skip_number_spin.setMinimum(1)
        self.evt_skip_number_spin.setMaximum(60)
        self.evt_skip_number_spin.setSingleStep(1)
        self.evt_skip_layout.addWidget(self.evt_skip_number_spin)
        self.evt_skip_combo = QtWidgets.QComboBox(Form)
        self.evt_skip_combo.setObjectName("evt_skip_combo")
        self.evt_skip_combo.addItem("Minutes")
        self.evt_skip_combo.addItem("Hours")
        self.evt_skip_combo.addItem("Days")
        self.evt_skip_combo.addItem("Weeks")
        self.evt_skip_combo.addItem("Months")
        self.evt_skip_combo.addItem("Years")
        self.evt_skip_layout.addWidget(self.evt_skip_combo)
        self.evt_formLayout.setLayout(8, QtWidgets.QFormLayout.SpanningRole, self.evt_skip_layout)
        self.evt_new_evt_button=QtWidgets.QPushButton(Form)
        self.evt_new_evt_button.setObjectName("evt_new_evt_button")
        self.evt_new_evt_button.setText("Add New Event")
        self.evt_formLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.evt_new_evt_button)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

class EventWidget(QtWidgets.QWidget):
    def __init__(self, parent, action_manager=None) -> None:
        super().__init__(parent)
        self.action_manager = action_manager

        self.ui = EventWidgetGui()
        self.ui.setupUi(self)

        self._lat = 0.0
        self._lon = 0.0

        self.ui.evt_next_sun_button.clicked.connect(self.next_suntime_button_clicked)
        self.ui.evt_next_evt_button.clicked.connect(self.next_event_button_clicked)
        self.ui.evt_skip_button.clicked.connect(self.skip_button_clicked)

    def set_lat_lon(self, latitude:float, longitude:float):
        self._lat = latitude
        self._lon = longitude

        self.ui.evt_lon_disp.setText("{:.4f}".format(longitude))
        self.ui.evt_lat_disp.setText("{:.4f}".format(latitude))

    def configure(self, action_manager):
        self.action_manager = action_manager
        self.action_manager.configure_event_widget(self)

    def update(self):
        time = self.action_manager.clock.time
        self.ui.evt_evt_table.clear()
        self.ui.evt_evt_table.setRowCount(0)
        self.parent

        for entry in self.action_manager.queue:
            evt_time = entry[0]
            event = entry[1]
            self._add_row_entry(evt_time, event.brief_desc)
        

        #self.ui.evt_date_disp.setText("{}{} of {} {}, {}:{:02d}".format(time.day+1,get_cardinal(time.day+1), time.month_str(), time.year+1, time.hour, time.minute))
        self.ui.evt_date_disp.setText("UMT: " + str(time))

        local_time = self.action_manager.clock.get_local_time(self._lon)
        #self.ui.local_date_disp.setText("{}{} of {} {}, {}:{:02d}".format(local_time.day+1,get_cardinal(local_time.day+1), 
        #                                    local_time.month_str(), local_time.year+1, local_time.hour, local_time.minute))
        self.ui.local_date_disp.setText("Local: " + str(local_time))

        next_suntime = str(self.action_manager.clock.get_next_suntime(self._lat, self._lon))
        if len(self.action_manager.queue)!=0:
            next_event = str(self.action_manager.queue[0][0])
            self.ui.evt_next_evt_button.setToolTip(next_event)
        self.ui.evt_next_sun_button.setToolTip(next_suntime)

    def _add_row_entry(self, date, description):
        """
        Adds an entry to the table
        """
        if not isinstance(date, Time):
            raise TypeError("Expected {} object, not {}".format(Time, type(date)))

        #self.evt_evt_table.setRowCount(self.evt_evt_table.rowCount()+1)
        #self.evt_evt_table.setColumnCount(self.evt_evt_table.columnCount()+1)

        insertion_row = 0
        
        #self.evt_evt_table.itemAt(1,1)

        if self.ui.evt_evt_table.rowCount()>0:
            while date > self.ui.evt_evt_table.itemAt(insertion_row, 0).time:
                insertion_row+=1
                if insertion_row==self.ui.evt_evt_table.rowCount():
                    break

        self.ui.evt_evt_table.insertRow(insertion_row)
        self.ui.evt_evt_table.setItem(insertion_row,0,TimeTableEntry(date))
        self.ui.evt_evt_table.setItem(insertion_row,1,QtWidgets.QTableWidgetItem(description))

    def skip_button_clicked(self):
        number = self.ui.evt_skip_number_spin.value()
        index = self.ui.evt_skip_combo.currentIndex()
        if index==0:
            time = Time(minute=number, date=False)
        elif index==1:
            time = Time(hour=number, date=False)
        elif index==2:
            time = Time(day=number, date=False)
        elif index==3:
            time = Time(day=number*days_in_week, date=False)
        elif index==4:
            time = Time(month=number, date=False)
        elif index==5:
            time = Time(year=number, date=False)
        else:
            raise ValueError("Not sure what to do with index {}".format(index))
        self.action_manager.skip_by_time(time)
        self.update()

    def next_event_button_clicked(self):
        self.action_manager.skip_to_next_event()
        self.update()

    def next_suntime_button_clicked(self):
        self.action_manager.skip_to_suntime()
        self.update()