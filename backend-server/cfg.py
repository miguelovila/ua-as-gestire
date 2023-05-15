import os

SERVER_PATH  = os.path.abspath(os.path.dirname(__file__))
STORAGE_PATH = os.path.normpath(os.path.join(SERVER_PATH, './storage'))
DB_PATH = os.path.normpath(os.path.join(STORAGE_PATH, './database.db'))
