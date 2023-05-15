import os

SERVER_PATH  = os.path.abspath(os.path.dirname(__file__))
STORAGE_PATH = os.path.normpath(os.path.join(SERVER_PATH, './storage'))
DB_PATH = os.path.normpath(os.path.join(STORAGE_PATH, './database.db'))
APP_SECRET = "hpUYY6QEHeDKAyoECAAQAzoRCC4QigUQsQ6CAgAEIAEEMsBOgYIABAWEB46CAgAE"