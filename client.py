import argparse
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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_address", help="server address", default=DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument("server_port", type=int, help="server port", default=DEFAULT_PORT, nargs="?")
    parser.add_argument("-m", "--mode", help="client mode", default="read", nargs="?")
    args = parser.parse_args()

    server_address = args.server_address
    server_port = args.server_port
    client_mode = args.mode

    if server_port < 1024 or server_port > 65535:
        logger.critical(f'Port should be in range 1024 to 65535. Port given is {server_port}')
        sys.exit(1)
    
    if not client_mode in ('read', 'send'):
        logger.critical(f"Client mode should be 'read' or 'send'. Mode given is {client_mode}")
        sys.exit(1)
    
    return server_address, server_port, client_mode


def main():
    # client 127.0.0.1 5555 -m send

    server_address, server_port, client_mode = get_args()

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
