"""Project constants"""
import logging

# Default port
DEFAULT_PORT = 7777
# Default IP for connect
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Max queue size
MAX_CONNECTIONS = 5
# Max message length (bytes)
MAX_PACKAGE_LENGTH = 1024
# Project encoding
ENCODING = 'utf-8'
# Logging level
LOG_LEVEL = logging.DEBUG

# Protocol JIM main keys:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
FROM = 'from'
TO = 'to'

# Protocol JIM other keys
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
ALERT = 'alert'
MESSAGE = 'msg'
MESSAGE_TEXT = 'message'
EXIT = "quit"
