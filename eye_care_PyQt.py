# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './pyqt.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.main.setWindowIcon(QtGui.QIcon('favicon.png'))
        self.time = "5 sec"


    def setupUi(self, MainWindow):
        # MainWindow.setWindowOpacity(0.5)

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(382, 133)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.vertical_button_layout = QtGui.QVBoxLayout()
        self.vertical_button_layout.setObjectName(_fromUtf8("vertical_button_layout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))

        self.horizontalLayout.addWidget(self.comboBox)
        self.start_button = QtGui.QPushButton(self.centralwidget)
        self.start_button.setEnabled(True)
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.horizontalLayout.addWidget(self.start_button)
        self.vertical_button_layout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.vertical_button_layout, 4, 0, 1, 1)
        self.vertical_progress_layout = QtGui.QVBoxLayout()
        self.vertical_progress_layout.setObjectName(_fromUtf8("vertical_progress_layout"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.vertical_progress_layout.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.vertical_progress_layout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 382, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):

        MainWindow.setWindowTitle(_translate("MainWindow", "Eye care", None))

        self.comboBox.setItemText(0, _translate("MainWindow", "5 sec", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "10 sec", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "1 min", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "20 min", None))
        self.comboBox.setItemText(4, _translate("MainWindow", "30 min", None))
        self.comboBox.setItemText(5, _translate("MainWindow", "40 min", None))
        self.comboBox.activated[str].connect(self.save_state)

        self.start_button.setText(_translate("MainWindow", "Start", None))


        self.start_button.clicked.connect(self.start_progress)

    def save_state(self, text):
        self.time = text
        self.progressBar.setValue(0)

    def convert_time(self, time):
        return float(time[:-3]) * 60 if time[-3:] == "min" else float(time[:-3])


    def start_progress(self):
        cur_time = time.time()

        time_to_stop = cur_time + self.convert_time(self.time)
        normalized_augment = 100/self.convert_time(self.time)

        completed = 0

        print("start", cur_time, "stop in", self.convert_time(self.time), "stop after", time_to_stop, "augment", normalized_augment)


        while cur_time < time_to_stop:
            cur_time = time.time()

            self.progressBar.setValue(round(completed))
            print(completed)
            print(round(completed))

            completed += normalized_augment
            time.sleep(1)

        else:
            print("end")




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

