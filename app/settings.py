# -*- coding: utf-8 -*-
import os

"""
Read enviroment variables from .env file
"""
from dotenv import load_dotenv
load_dotenv()

settings = {
    'SERVER_PORT': int(os.getenv('SERVER_PORT', 8050)),
    'DATA_PATH': os.getenv('DATA_PATH', 'data'),
    'LOGGER_NAME': os.getenv('LOGGER_NAME', 'app'),
    'LOGGER_LEVEL': os.getenv('LOGGER_LEVEL', 'INFO'),
    'LOGGER_PATH': os.getenv('LOGGER_PATH', 'logs'),
    'UPLOAD_PASSWORD':  os.getenv('UPLOAD_PASSWORD', '1111')
}
