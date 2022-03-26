import logging

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QRegularExpression, QCoreApplication
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QWidget, QPushButton, \
    QLineEdit, QTabWidget, QMessageBox

from src import WhiteTitleBar
from utils.dev import resize_window, open_database_connection


class AuthEmployer(object):
    def setupUi(self, MainWindow):
        self.main_window = MainWindow
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

        self.tab = QTabWidget(self.main_window)
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
        self.contact_line_edit.setValidator(QRegularExpressionValidator(QRegularExpression("[1-9]\\d{0,11}"), self.main_window))
        self.authorazation_formlayout.addRow("Phone number:", self.contact_line_edit)

        self.address_line_edit = QLineEdit()
        self.authorazation_formlayout.addRow("Address:", self.address_line_edit)

        self.authorazation_formlayout.addRow(" ", None)
        self.authorazation_formlayout.addRow(" ", None)

        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.setFixedSize(*self.SIZE_RATIO_LOGIN_WINDOW_PUSH_BUTTON)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.authorazation_formlayout.addRow(self.sign_up_button)


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
            QMessageBox.warning(self.main_window, "Error!", "Password and Validation password do not match!", QMessageBox.StandardButton.Ok)
            return

        name = self.name_line_edit.text()
        login = self.login_line_edit.text()
        contact = self.contact_line_edit.text()
        address = self.address_line_edit.text()

        if not (pswd and contact and address and name and login):
            QMessageBox.warning(self.main_window, "Error!", "Please fill in all the fields.",
                                QMessageBox.StandardButton.Ok)
        else:
            query = QSqlQuery()
            sql_ = f"INSERT INTO employer (name, login, pass, contact, address) VALUES {(name, login, pswd, contact, address)};"
            if query.exec(sql_):
                QMessageBox.information(self.main_window, "Success!", "You have successfully created an account! Now Please Log in.",
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
            sql_ = f"SELECT id FROM employer WHERE login = '{login}' and pass = '{pswd}';"

            if not query.exec(sql_):
                self.show_something_went_wrong_and_exit(query)

            while(query.next()):
                id_ = query.value(0)
                # TODO close the window and open the apps dashboard.
                return

        QMessageBox.warning(self.main_window, "Error!", "Wrong password or login.",
                            QMessageBox.StandardButton.Ok)

    def show_something_went_wrong_and_exit(self, query):
        logging.log(logging.INFO, query.lastError().text())
        QMessageBox.critical(self.main_window, "Error!",
                             "Oops, something went wrong! Check debug output for more details...",
                             QMessageBox.StandardButton.Ok)
        QCoreApplication.quit()
