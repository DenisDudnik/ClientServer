import json
import sys
import time
import logging
import log.config.client_log_config
from socket import socket, AF_INET, SOCK_STREAM
from decors import Log
from utils.const import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, PRESENCE, \
    TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT
from utils.func import get_message, send_message

logger = logging.getLogger('app.client')

@Log()
def create_presence(account_name='guest', status=''):
    '''Function create presence message'''
    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        "type": "status",
        USER: {
            ACCOUNT_NAME: account_name,
            "status": status
        }
    }
    logger.debug(f'Create presence message: {msg}')
    return msg


@Log()
def process_answer(msg: dict):
    '''Function process answer message'''
    logger.debug(f'Process message: {msg}')
    if RESPONSE in msg:
        # for 2xx messages
        if msg[RESPONSE] in range(200, 300):
            return f'{msg[RESPONSE]}: {msg.get(ALERT)}'
        # for other messages
        return f'{msg[RESPONSE]}: {msg.get(ERROR)}'
    raise ValueError


def main():
    # client 127.0.0.1 5555

    # try to find server address and port in args
    try:
        server_address = sys.argv[1]
    except IndexError:
        logger.warning("Server address wasn't found. Using default address")
        server_address = DEFAULT_IP_ADDRESS

    try:
        server_port = int(sys.argv[2])
    except IndexError:
        logger.warning("Server port wasn't found. Using default port")
        server_port = DEFAULT_PORT

    # init socket, connect, send message, get answer
    s = socket(AF_INET, SOCK_STREAM)
    try:
        logger.info(f'Connecting to {server_address}:{server_port}')
        s.connect((server_address, server_port))
    except Exception as e:
        logger.critical('Connection failed. Error: ', e)
    else:
        msg = create_presence(account_name='client1', status='I am here!')
        send_message(s, msg)
        try:
            data = get_message(s)
            logger.debug('From server: ', process_answer(data))
        except (ValueError, json.JSONDecodeError):
            logger.warning('Unknown message from server')
    finally:
        s.close()


if __name__ == '__main__':
    main()
