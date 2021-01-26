# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from logzero import logger


class MaskWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(0,0,0,102);')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.lb_desc = ''

    def show(self):
        """重写show，设置遮罩大小与parent一致
        """
        try:
            if self.parent() is None:
                return
            layout = QVBoxLayout()
            layout.setSizeConstraint(QLayout.SetMinimumSize)

            gif_label = QLabel()
            gif_label.setStyleSheet('background-color:transparent; color:white')
            gif = QMovie('./res/loading.gif')
            gif_label.setMovie(gif)
            gif.start()

            layout.addWidget(gif_label, 0, Qt.AlignHCenter)

            self.lb_desc = QLabel('')
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.white)
            pe.setColor(QPalette.Background, Qt.transparent)
            self.lb_desc.setPalette(pe)
            self.lb_desc.setFont(QFont('Roman times', 10, QFont.Bold))

            self.lb_desc.setAlignment(Qt.AlignCenter)
            self.lb_desc.setFixedHeight(100)
            layout.addWidget(self.lb_desc)

            self.setLayout(layout)
            parent_rect = self.parent().geometry()
            self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
            super().show()
        except Exception as e:
            logger.error(e)

    def set_msg(self, msg):
        if self.lb_desc is not None and self.lb_desc != '':
            self.lb_desc.setText(msg)
