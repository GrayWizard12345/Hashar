import os

from root_file import ROOT_DIR

DATABASE_CONFIG = os.path.join(ROOT_DIR, 'static/config.ini')
FAVORITES_CONFIG = os.path.join(ROOT_DIR, 'static/favorites.ini')

UI_LOG_FILE = os.path.join(ROOT_DIR, 'logs/ui_debug.log')

DATABASE_LOG_FILE = os.path.join(ROOT_DIR, 'logs/database_init_debug.log')

# Images for tableView
STATIC_DIR = os.path.join(ROOT_DIR, os.path.normpath('static/'))

SVG_DIR = os.path.join(ROOT_DIR, os.path.normpath('static/svg/'))
