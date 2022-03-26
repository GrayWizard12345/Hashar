"""
dev.py
This file contains utilities that make development process less painful
"""
import configparser
import inspect
import logging
import sys
from enum import Enum

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QWidget

from utils import DATABASE_CONFIG

def setup_logging(filename=None):
    """
    If filename is not provided, the logging output is redirected to stdout only. Otherwise, it is written to the
    file as well. The file open mode is append, so file will grow indefinitely.
    :param filename: a path to a logging file.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(filename)s: Line: %(lineno)d - %(levelname)s - %(message)s')

    if filename:
        file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)

    stdout_handler.setFormatter(formatter)
    root.addHandler(stdout_handler)


def resize_widget(width: int, height: int, widget: QWidget, set_max=False, set_min=False):
    """
    Resize
    :param width: a new width to be applied to the widget.
    :param height: a new height to be applied to the widget.
    :return:
    """
    widget.resize(width, height)
    if set_max:
        widget.setMaximumSize(width, height)

    if set_min:
        widget.setMaximumSize(width, height)
    return widget


def resize_window(window):
    """
    Resizes the window to 720x480 px.
    This method also translates the window into the center of the primary monitor.
    :return:
    """

    desk_rect = QGuiApplication.primaryScreen().availableGeometry()
    resize_widget(720, 480, window)
    desk_x = desk_rect.width()
    desk_y = desk_rect.height()

    window.move(desk_x // 2 - window.geometry().width() // 2, desk_y // 2 - window.geometry().height() // 2)

    return window

DATABASE = None

def open_database_connection(database_name: str = None, username: str = None, password: str = None):
    """
    Opens a connection to the database if the database is not open.
    :return: open QSqlDatabase
    """
    # TODO change function to utilize parameters from its signature
    # TODO Warn user about Database connection error.

    global DATABASE

    if (DATABASE is not None) and DATABASE.isOpen() and DATABASE.isValid():
        return DATABASE

    if not DATABASE:
        config = configparser.ConfigParser()
        config.read(DATABASE_CONFIG)
        host = config['postgresql']['host']
        port = config['postgresql']['port']
        database_name = config['postgresql']['database']
        user = config['postgresql']['user']
        password = config['postgresql']['password']

        DATABASE = QSqlDatabase.addDatabase('QPSQL')
        DATABASE.setHostName(host)
        DATABASE.setPort(eval(port))
        DATABASE.setDatabaseName(database_name)
        DATABASE.setUserName(user)
        DATABASE.setPassword(password)
        ok = DATABASE.open()

        if not ok:
            logging.debug(DATABASE.lastError().text() + " - dev.py")

    if not DATABASE.isOpen():
        ok = DATABASE.open()
        if not ok:
            logging.debug(DATABASE.lastError().text() + " - dev.py DATABASE.open() failed.")

    return DATABASE


