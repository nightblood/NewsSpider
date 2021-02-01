from mask_layout import MaskWidget
from 浙江日报 import zjrb
from 人民日报 import rmrb
from 绍兴日报 import sxrb
import datetime
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        MainWindow.setFixedSize(self, 500, 300)
        self.setWindowTitle('新闻抓取工具')
        self.setGeometry(500, 300, 300, 200)
        self.worker = None
        self.keywords = ''
        self.start_dt = datetime.datetime.now().strftime('%Y-%m/%d')
        self.end_dt = datetime.datetime.now().strftime('%Y-%m/%d')
        self.init_window()

    def init_window(self):
        self.main_layout = QVBoxLayout(self)
        self.l_desc = QLabel('新闻抓取工具\n人民日报、浙江日报。')
        # self.pte_staff = QLabel(self.get_staff_str())
        # self.pte_staff.setFont(QFont('Roman times', 14, QFont.Bold))
        self.lb_holiday_desc = QLabel()
        self.l_start_dt = QLabel('开始日期')
        self.l_end_dt = QLabel('结束日期')
        self.l_keywords = QLabel('关键字')
        self.dte_start = QDateTimeEdit(QDate.currentDate(), self)
        self.dte_start.dateTimeChanged.connect(lambda: self.set_time(1))
        self.dte_start.setDisplayFormat('yyyy-MM/dd')
        self.dte_start.setCalendarPopup(True)
        self.dte_end = QDateTimeEdit(QDate.currentDate(), self)
        self.dte_end.dateTimeChanged.connect(lambda: self.set_time(2))
        self.dte_end.setDisplayFormat('yyyy-MM/dd')
        self.dte_end.setCalendarPopup(True)
        self.qle_keywords = QLineEdit()

        self.layout_start_dt = QSplitter(Qt.Horizontal)
        self.layout_end_dt = QSplitter(Qt.Horizontal)
        self.layout_func = QSplitter(Qt.Horizontal)
        self.layout_keywords = QSplitter(Qt.Horizontal)

        self.btn_export = QPushButton('开始抓取')
        self.layout_func.addWidget(self.btn_export)

        self.layout_start_dt.setFixedHeight(2)

        self.btn_export.clicked.connect(self.on_export)

        self.layout_start_dt.addWidget(self.l_start_dt)
        self.layout_start_dt.addWidget(self.dte_start)
        self.layout_end_dt.addWidget(self.l_end_dt)
        self.layout_end_dt.addWidget(self.dte_end)
        self.layout_keywords.addWidget(self.l_keywords)
        self.layout_keywords.addWidget(self.qle_keywords)

        self.main_layout.addWidget(self.l_desc)
        # self.main_layout.addWidget(self.pte_staff)
        # self.main_layout.addWidget(self.layout_miss)
        self.main_layout.addWidget(self.layout_start_dt)
        self.main_layout.addWidget(self.layout_end_dt)
        # self.main_layout.addWidget(self.l_weeks)
        self.main_layout.addWidget(self.layout_keywords)
        self.main_layout.addWidget(self.layout_func)

    def on_export(self):
        if self.start_dt > self.end_dt:
            QMessageBox.question(self, '提示', '起始日期不能大于结束日期', QMessageBox.Yes)
            return
        self.keywords = self.qle_keywords.text()
        if self.keywords is None or self.keywords == '':
            QMessageBox.question(self, '提示', '关键字不能为空', QMessageBox.Yes)
            return
        self.export_worker = ExportWorker(self.start_dt, self.end_dt, self.keywords)
        self.export_worker.started.connect(self.show_mask)
        self.export_worker.sig_complete.connect(self.export_complete)
        self.export_worker.sig_failed.connect(self.export_failed)
        self.export_worker.finished.connect(self.hide_mask)
        self.export_worker.start()

    def hide_mask(self):
        if self.mask is not None and self.mask != "":
            self.mask.close()

    def export_failed(self, desc):
        try:
            QMessageBox.question(self, '错误', desc, QMessageBox.Yes)
        except Exception as e:
            print(e)

    def export_complete(self, desc):
        try:
            QMessageBox.question(self, '提示', desc, QMessageBox.Yes)
        except Exception as e:
            print(e)

    def show_mask(self):
        self.mask = MaskWidget(self)
        self.mask.show()
        self.mask.set_msg("抓取中。。。")

    def set_time(self, btn_idx):
        if btn_idx == 1:
            self.start_dt = self.dte_start.text()
        else:
            self.end_dt = self.dte_end.text()
        # print(self.start_dt, self.end_dt)
        # print(self.start_dt, self.end_dt)
        # self.l_weeks.setText('共' + str(self.get_delta_weeks()) + '周')


class ExportWorker(QThread):
    sig_complete = pyqtSignal(str)
    sig_failed = pyqtSignal(str)

    def __init__(self, start_dt, end_dt, keywords):
        super().__init__()
        self.end_dt = end_dt
        self.start_dt = start_dt
        self.keywords = keywords

    def run(self):
        try:
            time.sleep(4)
            today = datetime.datetime.now().strftime('%Y%m%d')
            file = '新闻{0}.xlsx'.format(today)
            zjrb(self.start_dt, self.end_dt, self.keywords)
            rmrb(self.start_dt, self.end_dt, self.keywords)
            sxrb(self.start_dt, self.end_dt, self.keywords)
            self.sig_complete.emit('抓取完成，生成文件《{0}》'.format(file))
        except Exception as e:
            print(e)
            self.sig_failed.emit(str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    icon = QIcon()
    icon.addPixmap(QPixmap('icon.ico'), QIcon.Normal, QIcon.Off)
    window.setWindowIcon(icon)

    window.show()
    sys.exit(app.exec_())

    # today = datetime.datetime.now().strftime('%Y-%m/%d')
    # print('1. 请输入起始日期（默认 {0}）：\n'.format(today))
    # start_dt = input()
    # print('2. 请输入结束日期（默认 {0}）：\n'.format(today))
    # end_dt = input()
    # print('3. 请输入要搜索的关键字：\n')
    # key_words = input()
    # print('开始搜索起始日期{0} 到 {1}且关键字为{2}的新闻。'.format(start_dt, end_dt, key_words))
    # zjrb(start_dt, end_dt, key_words)
    # rmrb(start_dt, end_dt, key_words)

