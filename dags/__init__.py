import os

_PATH_DIRECTORY_FILES = f"{os.path.dirname(os.path.abspath(__file__)).split('dags')[0]}"
PATH_FILE_LANDING = f"{_PATH_DIRECTORY_FILES}/temp/landing"
PATH_FILE_PROCESSING = f"{_PATH_DIRECTORY_FILES}/temp/processing"
PATH_FILE_SILVER = f"{_PATH_DIRECTORY_FILES}/temp/silver"
