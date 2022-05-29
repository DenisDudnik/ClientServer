import argparse
import sys
import json
import logging
import log.config.server_log_config
from socket import socket, AF_INET, SOCK_STREAM
from decors import Log, log_dec
from utils.const import ENCODING, DEFAULT_PORT, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT
from utils.func import get_message, send_message

logger = logging.getLogger('app.server')

@log_dec
def create_response(msg):
    '''Function to create a response'''
    logger.debug(f'Process message: {msg}')
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg \
            and msg[USER][ACCOUNT_NAME] == 'client1':
        # and msg[USER][ACCOUNT_NAME] in contact_list:
        msg = {
            RESPONSE: 200,
            ALERT: "OK"
        }
    else:
        msg = {
            RESPONSE: 400,
            ERROR: "Bad Request"
        }
    logger.info(f'Create response: {msg}')
    return msg


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="server address", default="", nargs="?")
    parser.add_argument("-p", "--port", type=int, help="server port", default=DEFAULT_PORT, nargs="?")
    args = parser.parse_args()

    server_address = args.address
    server_port = args.port

    if server_port < 1024 or server_port > 65535:
        logger.critical(f'Port should be in range 1024 to 65535. Port given is {server_port}')
        sys.exit(1)
    
    return server_address, server_port


def main():
    # server -p 5555 -a 127.0.0.1

    server_address, server_port = get_args()

    s = socket(AF_INET, SOCK_STREAM)
    server_address_pair = (server_address, server_port)
    try:
        s.bind(server_address_pair)
        logger.info('Server starting with IP "{}" and PORT "{}"'.format(*server_address_pair))
    except OSError as e:
        logger.error('Error open socket. Error: {e}')
    else:
        s.listen(MAX_CONNECTIONS)
        logger.info(f'Server was run on {server_address}:{server_port}')

        while True:
            client, addr = s.accept()
            try:
                data = get_message(client)
                logger.info(f'From: {addr} => {data}')
                msg = create_response(data)
                send_message(client, msg)
            except (ValueError, json.JSONDecodeError):
                logger.error('Unknown message from server')
            finally:
                client.close
    finally:
        s.close()
        logger.info('Server was stopped')


if __name__ == '__main__':
    main()
