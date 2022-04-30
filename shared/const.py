"""Project constants"""

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

# Protocol JIM main keys:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Protocol JIM other keys
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
ALERT = 'alert'
