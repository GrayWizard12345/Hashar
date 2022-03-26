import logging
import os
import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QPoint, QRegularExpression, QCoreApplication
from PyQt6.QtGui import QMouseEvent, QPixmap, QIcon, QFont, QRegularExpressionValidator, QIntValidator
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, \
    QLineEdit, QTabWidget, QSpacerItem, QMessageBox, QButtonGroup, QRadioButton

from utils.dev import setup_logging, resize_window, open_database_connection
from utils.pathfinder import UI_LOG_FILE, SVG_DIR


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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.init_sizes()
        open_database_connection()
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
        self.level0.setContentsMargins(20, 0, 20, 20)
        self.level0.setObjectName("level0")

        self.title_bar_layout = QtWidgets.QHBoxLayout()
        self.title_bar_layout.setObjectName("title_bar_layout")
        self.title_bar_layout.addWidget(WhiteTitleBar(MainWindow))

        self.level0.addLayout(self.title_bar_layout)

        self.tab = QTabWidget(main_window)
        self.tab.setTabBarAutoHide(True)

        self.init_authorization_tab()
        self.init_authentication_tab()

        self.tab.addTab(self.authentication, "Login")
        self.tab.addTab(self.authorazation, "Sign Up")

        self.level0.addWidget(self.tab)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_authorization_tab(self):
        self.authorazation = QWidget()
        self.authorazation_formlayout = QtWidgets.QFormLayout(self.authorazation)
        self.authorazation_formlayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.authorazation_formlayout.setObjectName("authorazation_formlayout")
        self.authorazation_formlayout.setContentsMargins(25, 50, 27, 20)
        self.create_authorization_form()

    def init_authentication_tab(self):
        self.authentication = QWidget()
        self.authentication_formlayout = QtWidgets.QFormLayout(self.authentication)
        self.authentication_formlayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.authentication_formlayout.setObjectName("authentication_formlayout")
        self.authentication_formlayout.setContentsMargins(25, 50, 27, 20)
        self.create_authentication_form()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


    def init_sizes(self):
        main_screen_width = 1440
        main_screen_height = 900
        self.SIZE_RATIO_LOGIN_WINDOW = 0.5, 0.5
        self.SIZE_RATIO_LOGIN_WINDOW_LINE_EDIT = int(main_screen_width * 0.13), int(main_screen_height * 0.028)
        self.SIZE_RATIO_LOGIN_WINDOW_PUSH_BUTTON = int(main_screen_width * 0.058), int(main_screen_height * 0.0278)
        self.SIZE_RATIO_LOGIN_WINDOW_SPACING = int(main_screen_height * 0.0138)

    def create_authorization_form(self):
        self.login_line_edit = QLineEdit()
        self.authorazation_formlayout.addRow("Create Login:", self.login_line_edit)

        self.password_box = QLineEdit()
        self.password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.authorazation_formlayout.addRow("Create Password:", self.password_box)

        self.password_validation_box = QLineEdit()
        self.password_validation_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.authorazation_formlayout.addRow("Validate Password:", self.password_validation_box)

        self.name_line_edit = QLineEdit()
        self.authorazation_formlayout.addRow("Name:", self.name_line_edit)

        self.contact_line_edit = QLineEdit()
        self.contact_line_edit.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,11}"), main_window))
        self.authorazation_formlayout.addRow("Phone number:", self.contact_line_edit)

        self.address_line_edit = QLineEdit()
        self.authorazation_formlayout.addRow("Address:", self.address_line_edit)

        self.age_line_edit = QLineEdit()
        self.age_line_edit.setValidator(QIntValidator(18, 100, main_window))
        self.authorazation_formlayout.addRow("Age:", self.age_line_edit)

        self.price_line_edit = QLineEdit()
        self.price_line_edit.setValidator(
            QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,11}"), main_window))
        self.authorazation_formlayout.addRow("Hourly Service Price:", self.price_line_edit)

        self.create_gender_picker_row()

        self.authorazation_formlayout.addRow(" ", None)
        self.authorazation_formlayout.addRow(" ", None)

        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.setFixedSize(*self.SIZE_RATIO_LOGIN_WINDOW_PUSH_BUTTON)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.authorazation_formlayout.addRow(self.sign_up_button)

    def create_gender_picker_row(self):
        self.gender_picker = QWidget(main_window)
        layout_ = QHBoxLayout(self.gender_picker)

        self.gender_picker_button_group = QButtonGroup(self.gender_picker)
        male = QRadioButton("Male")

        self.gender_picker_button_group.addButton(male)
        female = QRadioButton("Female")

        self.gender_picker_button_group.addButton(female)

        layout_.addWidget(male)
        layout_.addWidget(female)
        self.authorazation_formlayout.addRow("Gender:", self.gender_picker)

    def create_authentication_form(self):
        self.auth_login_line_edit = QLineEdit()
        self.authentication_formlayout.addRow("Login:", self.auth_login_line_edit)

        self.auth_password_box = QLineEdit()
        self.auth_password_box.setEchoMode(QLineEdit.EchoMode.Password)
        self.authentication_formlayout.addRow("Password:", self.auth_password_box)

        self.authentication_formlayout.addRow(" ", None)
        self.authentication_formlayout.addRow(" ", None)

        self.login_button = QPushButton("Login")
        self.login_button.setFixedSize(*self.SIZE_RATIO_LOGIN_WINDOW_PUSH_BUTTON)
        self.login_button.clicked.connect(self.log_in)
        self.authentication_formlayout.addRow(self.login_button)

    def sign_up(self):

        pswd = self.password_box.text()
        pswd_vald = self.password_validation_box.text()

        if pswd_vald != pswd:
            QMessageBox.warning(main_window, "Error!", "Password and Validation password do not match!", QMessageBox.StandardButton.Ok)
            return

        name = self.name_line_edit.text()
        login = self.login_line_edit.text()
        contact = self.contact_line_edit.text()
        address = self.address_line_edit.text()
        age = self.age_line_edit.text()
        price = self.price_line_edit.text()

        is_male = self.gender_picker_button_group.buttons()[0].isChecked()
        gender = "M" if is_male else "W"

        if not (pswd and contact and address and name and login and age and price and gender):
            QMessageBox.warning(main_window, "Error!", "Please fill in all the fields.",
                                QMessageBox.StandardButton.Ok)
        else:
            query = QSqlQuery()
            sql_ = f"INSERT INTO employee (name, login, pass, contact, address, price, age, gender) VALUES {(name, login, pswd, contact, address, price, age, gender)};"
            if query.exec(sql_):
                QMessageBox.information(main_window, "Success!", "You have successfully created an account! Now Please Log in.",
                                    QMessageBox.StandardButton.Ok)
                self.tab.setCurrentIndex(0)
                self.clear_sign_up_fields()
            else:
                self.show_something_went_wrong_and_exit(query)

    def clear_sign_up_fields(self):
        self.contact_line_edit.clear()
        self.name_line_edit.clear()
        self.address_line_edit.clear()
        self.login_line_edit.clear()
        self.password_box.clear()
        self.password_validation_box.clear()

    def log_in(self):
        pswd = self.auth_password_box.text()
        login = self.auth_login_line_edit.text()

        if login and pswd:
            query = QSqlQuery()
            sql_ = f"SELECT id FROM employee WHERE login = '{login}' and pass = '{pswd}';"

            if not query.exec(sql_):
                self.show_something_went_wrong_and_exit(query)

            while(query.next()):
                id_ = query.value(0)
                # TODO close the window and open the apps dashboard.
                return

        QMessageBox.warning(main_window, "Error!", "Wrong password or login.",
                            QMessageBox.StandardButton.Ok)

    def show_something_went_wrong_and_exit(self, query):
        logging.log(logging.INFO, query.lastError().text())
        QMessageBox.critical(main_window, "Error!",
                             "Oops, something went wrong! Check debug output for more details...",
                             QMessageBox.StandardButton.Ok)
        QCoreApplication.quit()


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
