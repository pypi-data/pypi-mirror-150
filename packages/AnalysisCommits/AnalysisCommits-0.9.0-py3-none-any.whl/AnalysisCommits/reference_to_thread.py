# pip install pyqt5

import logging
import os
import sys
import time
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import *

DISPLAY_LOG_IN_TERMNINAL = True

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s (%(funcName)20s:%(lineno)4d) [%(levelname)s]: %(message)s')

# Print in terminal
if DISPLAY_LOG_IN_TERMNINAL:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# Write in file
today = datetime.now()
today = today.strftime('%Y_%m_%d')
filename = '%s.log' % today

# If file exist, remove it
if os.path.isfile(filename):
    os.remove(filename)

file_handler = logging.FileHandler(filename)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class MainDialog(QDialog):
    def __init__(self, fn=None ,parent=None):
        # Display minimize, close button
        super(MainDialog, self).__init__(parent, flags=Qt.WindowMinimizeButtonHint |Qt.WindowCloseButtonHint)
        uic.loadUi("./main.ui", self)

        self.my_thread = None

        self.btn_exit.clicked.connect(self.close_dialog)


        # Thread
        self.btn_start.clicked.connect(self.start_thread)
        self.btn_stop.clicked.connect(self.stop_thread)

        # Line Edit
        self.btn_get_le.clicked.connect(self.get_le)
        self.btn_set_le.clicked.connect(self.set_le)

        # Spin Box
        self.btn_get_sp.clicked.connect(self.get_sp)
        self.btn_set_sp.clicked.connect(self.set_sp)

        # Radio Button
        self.btn_get_rb.clicked.connect(self.get_rb)
        self.btn_set_rb.clicked.connect(self.set_rb)

        # List Widget
        self.lw_count = 0
        self.btn_add_list.clicked.connect(self.add_lw)
        self.btn_remove_list.clicked.connect(self.delete_lw)
        self.listWidget.clicked.connect(self.select_row_lw)
        self.btn_get_list.clicked.connect(self.get_list_lw)

        # Table Widget
        self.tableWidgetInit()
        self.btn_get_tablewidget_item.clicked.connect(self.get_item)

        # MessageBox
        self.btn_information.clicked.connect(self.box_info)
        self.btn_warning.clicked.connect(self.box_warning)
        self.btn_question.clicked.connect(self.box_question)

        # Disable, Enable
        self.btn_enable.clicked.connect(self.enable_exit_button)
        self.btn_disable.clicked.connect(self.disble_exit_button)

        self.show()

    ####################################################################
    # Enable/Disable Button
    def enable_exit_button(self):
        self.btn_exit.setEnabled(True)

    def disble_exit_button(self):
        self.btn_exit.setEnabled(False)

    ######################################################################################
    # MessageBox
    def box_question(self):
        result = QMessageBox.question(self, 'Qeustion', 'Do you delete?', QMessageBox.Yes, QMessageBox.No)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    def box_warning(self):
        result = QMessageBox.warning(self, 'Warning', 'Wrong Information', QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    def box_info(self):
        result = QMessageBox.information(self, 'Information', 'Success', QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.add_log('Yes')
        else:
            self.add_log('No')

    ###########################################################################################
    # TableWidget
    def tableWidgetInit(self):
        columns = 'Name;Address;Age'
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(columns.split(';'))
        # self.tableWidget.setColumnWidth(0, 89)
        # self.tableWidget.setColumnWidth(1, 100)
        # self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setRowCount(3)

        table_data = [['Kim', 'Seoul', '20'], ['Park', 'Busan', '20'], ['Lee', 'Daegu', '20']]

        for i in range(3):
            data = table_data[i]
            for j in range(len(data)):
                item = QTableWidgetItem(data[j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)

    def get_item(self):
        row = int(self.le_row.text())
        column = int(self.le_column.text())
        self.add_log('TableWidget Item[%s,%s]: %s' % (row, column, self.tableWidget.item(row, column).text()))
    ###########################################################################################
    # ListWidget
    def add_lw(self):
        self.lw_count += 1
        self.listWidget.addItem('Hello:%s' % self.lw_count)

    def delete_lw(self):
        current_row = self.listWidget.currentRow()
        self.listWidget.takeItem(current_row)

    def select_row_lw(self):
        current_row = self.listWidget.currentRow()
        self.add_log('CurrentRow: %s' % current_row)

    def get_list_lw(self):
        items = []
        for i in range(self.listWidget.count()):
            items.append(self.listWidget.item(i).text())
        self.add_log('ListWidget: %s' % items)
    ###########################################################################################
    # LineEdit
    def get_le(self):
        value = self.lineEdit.text()
        self.add_log('LineEdit: %s' % value)

    def set_le(self):
        self.lineEdit.setText('world')
    ###########################################################################################
    # SpinBox
    def get_sp(self):
        value = self.spinBox.value()
        self.add_log('SpinBox: %s' % value)

    def set_sp(self):
        self.spinBox.setValue(10)
    ###########################################################################################
    # RadioButton
    def get_rb(self):
        value = self.radioButton_a.isChecked()
        self.add_log('RadioButton A: %s' % value)
        value = self.radioButton_b.isChecked()
        self.add_log('RadioButton B: %s' % value)
        value = self.checkBox.isChecked()
        self.add_log('CheckBox: %s' % value)

    def set_rb(self):
        self.radioButton_a.setChecked(True)
        self.radioButton_b.setChecked(False)
        self.checkBox.setChecked(True)
    ###########################################################################################
    # For Thread
    def start_thread(self):
        try:
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(100)
            self.progressBar.setValue(0)

            interval = 0.1
            self.my_thread = SomethingThread(None, interval)
            self.my_thread.logSignal.connect(self.add_log)
            self.my_thread.stopSignal.connect(self.thread_is_stopped)
            self.my_thread.countSignal.connect(self.count)
            self.my_thread.start()

            self.set_enable_buttons(False)
        except Exception as e:
            print('--> Exception is "%s" (Line: %s)' % (e, sys.exc_info()[-1].tb_lineno))

    def stop_thread(self):
        if self.my_thread is not None:
            self.my_thread.stop()

    def set_enable_buttons(self, enable):
        self.btn_start.setEnabled(enable)
        self.btn_stop.setEnabled(not enable)
    ###########################################################################################
    # Signal pyqtslot
    @pyqtSlot(int)
    def count(self, count):
        self.add_log('ProgressBar Value: %s' % count)
        self.progressBar.setValue(count)

    @pyqtSlot()
    def thread_is_stopped(self):
        self.set_enable_buttons(True)

    @pyqtSlot(str)
    def add_log(self, message):
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        log_message = '[%s]: %s' % (now, message)
        self.tb_log.append(log_message)
        logger.info(message)
    ###########################################################################################

    def close_dialog(self):
        sys.exit(0)

    # ESC 무시
    def key_press_event(self, event):
        if not event.key() == Qt.Key_Escape:
            pass

class SomethingThread(QThread):
    logSignal = pyqtSignal(str)
    countSignal = pyqtSignal(int)
    stopSignal = pyqtSignal()

    def __init__(self, param, interval=10):
        super(self.__class__, self).__init__()
        self.param = param
        self.isRunning = True
        self.interval = interval

    def run(self):
        self.logSignal.emit('Thread is started')
        count = 1
        while self.isRunning:
            time.sleep(self.interval)
            self.countSignal.emit(count)
            count += 1

        self.logSignal.emit('Thread is stopped')
        self.stopSignal.emit()

    def stop(self):
        self.isRunning = False
        self.logSignal.emit('Thread is stopping')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainDialog()
    myWindow.show()
    app.exec()