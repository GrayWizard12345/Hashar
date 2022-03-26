import os

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


from utils import SVG_DIR


class WhiteTitleBar(QWidget):
    def __init__(self, parent):
        super(WhiteTitleBar, self).__init__()
        self.parent = parent

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.setSizePolicy(sizePolicy)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 10, 0)
        self.title = QLabel("")

        btn_size = 14

        self.btn_close = QPushButton(QIcon(os.path.join(SVG_DIR, 'btn_close_window.svg')), None)

        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setFlat(True)

        self.btn_min = QPushButton(QIcon(os.path.join(SVG_DIR, 'btn_minimize_window.svg')), None)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setFlat(True)


        self.title.setFixedHeight(16)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_placeholder_label = QtWidgets.QLabel(self)
        logo_pixmap = QPixmap(os.path.join(SVG_DIR, 'logo.svg'))

        self.logo_placeholder_label.setPixmap(logo_pixmap)
        self.logo_placeholder_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.logo_placeholder_label.setObjectName("logo_placeholder")
        self.logo_placeholder_label.setFixedSize(70, 50)
        self.logo_placeholder_label.setStyleSheet("border:0; margin:0;padding:0;")
        self.layout.addWidget(self.logo_placeholder_label)

        self.program_name_label = QtWidgets.QLabel(self)
        self.program_name_label.setObjectName("program_label")
        self.program_name_label.setText("Hashar")
        self.program_name_label.setStyleSheet("border:0; margin:0;padding:0; color:#3662BC; font-size: 10px;")
        self.program_name_label.setFixedHeight(16)
        self.layout.addWidget(self.program_name_label)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        # self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: rgba(255,255,255, 150);
            color: white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(WhiteTitleBar, self).resizeEvent(QResizeEvent)
        # self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event: QMouseEvent):
        self.pressing = True
        self.start = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressing:
            self.end = event.globalPosition().toPoint()
            self.parent.move(self.end - self.start)

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()
