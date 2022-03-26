import os
import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QPoint, QRegularExpression
from PyQt6.QtGui import QMouseEvent, QPixmap, QIcon, QFont, QRegularExpressionValidator, QIntValidator
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, \
    QLineEdit

from utils.dev import setup_logging, resize_window
from utils.pathfinder import UI_LOG_FILE, SVG_DIR


class WhiteTitleBar(QWidget):
    def __init__(self, parent):
        super(WhiteTitleBar, self).__init__()
        self.parent = parent

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.setSizePolicy(sizePolicy)
        print(self.parent.width())
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
        self.program_name_label.setText("Hashar - Ishchi")
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.init_sizes()
        resize_window(MainWindow)
        MainWindow.setObjectName("MainWindow")

        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)

        MainWindow.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        MainWindow.setAcceptDrops(False)
        MainWindow.setObjectName("MainWindow")
        # MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)

        # Transparent background of the window for debug purposes
        MainWindow.setStyleSheet("background-color: rgba(255, 255, 255, 255)")

        self.level0 = QtWidgets.QVBoxLayout(MainWindow)
        self.level0.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.level0.setContentsMargins(0, 0, 0, 0)
        self.level0.setObjectName("level0")

        self.title_bar_layout = QtWidgets.QHBoxLayout()
        self.title_bar_layout.setObjectName("title_bar_layout")
        self.title_bar_layout.addWidget(WhiteTitleBar(MainWindow))

        self.level0.addLayout(self.title_bar_layout)

        self.lvl_1_main_formlayout = QtWidgets.QFormLayout()
        self.lvl_1_main_formlayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.lvl_1_main_formlayout.setObjectName("lvl_1_main_verticallayout")
        self.lvl_1_main_formlayout.setContentsMargins(25, 50, 27, 20)

        self.create_authorization_form()
        self.level0.addLayout(self.lvl_1_main_formlayout)
        self.level0.setStretch(1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def init_sizes(self):
        main_screen_width = 1440
        main_screen_height = 900
        self.SIZE_RATIO_LOGIN_WINDOW = 0.5, 0.5
        self.SIZE_RATIO_LOGIN_WINDOW_LINE_EDIT = int(main_screen_width * 0.13), int(main_screen_height * 0.028)
        self.SIZE_RATIO_LOGIN_WINDOW_PUSH_BUTTON = int(main_screen_width * 0.052), int(main_screen_height * 0.0278)
        self.SIZE_RATIO_LOGIN_WINDOW_SPACING = int(main_screen_height * 0.0138)
        print(self.SIZE_RATIO_LOGIN_WINDOW_SPACING)

    def create_authorization_form(self):
        self.login_line_edit = QLineEdit()
        self.lvl_1_main_formlayout.addRow("Create Login:", self.login_line_edit)

        self.password_box = QLineEdit()
        self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.lvl_1_main_formlayout.addRow("Create Password:", self.password_box)

        self.password_validation_box = QLineEdit()
        self.password_validation_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.lvl_1_main_formlayout.addRow("Validate Password:", self.password_validation_box)

        self.name_line_edit = QLineEdit()
        self.lvl_1_main_formlayout.addRow("Name:", self.name_line_edit)

        self.contact_line_edit = QLineEdit()
        self.contact_line_edit.setValidator(
            QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,11}"), main_window))
        self.lvl_1_main_formlayout.addRow("Phone number:", self.contact_line_edit)

        self.age_line_edit = QLineEdit()
        self.age_line_edit.setValidator(QIntValidator(18, 100, main_window))
        self.lvl_1_main_formlayout.addRow("Age:", self.age_line_edit)

        self.price_line_edit = QLineEdit()
        self.price_line_edit.setValidator(
            QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,11}"), main_window))
        self.lvl_1_main_formlayout.addRow("Hourly Service Price:", self.price_line_edit)


if __name__ == '__main__':
    setup_logging(UI_LOG_FILE)
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QFont("Gilroy", 12))

    main_window = QtWidgets.QWidget()

    window = Ui_MainWindow()
    window.setupUi(main_window)
    main_window.show()
    # myWin = MyMainWindows()
    # myWin.show()
    sys.exit(app.exec())
