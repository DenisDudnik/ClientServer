import argparse
import sys
import json
import logging
import log.config.server_log_config
import select
from socket import socket, AF_INET, SOCK_STREAM
from decors import Log, log_dec
from utils.const import ENCODING, DEFAULT_PORT, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT, MESSAGE, \
        MESSAGE_TEXT
from utils.func import get_message, send_message

logger = logging.getLogger('app.server')

@log_dec
def create_response(msg, client, message_list):
    '''Function to create a response'''
    logger.debug(f'Process message: {msg}')

    # valid presense message
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg \
            and msg[USER][ACCOUNT_NAME] == 'client1':
        # and msg[USER][ACCOUNT_NAME] in contact_list:
        msg = {
            RESPONSE: 200,
            ALERT: "OK"
        }
    # text messages (we shouldn't process msg, just resend to client or chat)
    elif ACTION in msg and msg[ACTION] == MESSAGE and TIME in msg and 'from' in msg and MESSAGE_TEXT in msg:
            message_list.append(msg)
            # TODO: here we should create message for author (response 200)
    # bad message
    else:
        msg = {
            RESPONSE: 400,
            ERROR: "Bad Request"
        }
    logger.info(f'Create response: {msg}')
    if client:
        send_message(client, msg)
    return msg


@log_dec
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
        s.settimeout(0.2)
        logger.info('Server starting with IP "{}" and PORT "{}"'.format(*server_address_pair))
    except OSError as e:
        logger.error('Error open socket. Error: {e}')
    else:
        s.listen(MAX_CONNECTIONS)
        logger.info(f'Server was run on {server_address}:{server_port}')

        clients, messages = [], []

        while True:
            try:            
                client, addr = s.accept()
            except OSError:
                pass
            else:
                logger.info(f'Client connected {addr}')
                clients.append(client)
            
            recv_lst, send_lst, err_lst = [], [], []

            try:
                if clients:
                    recv_lst, send_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            if recv_lst:
                for client in recv_lst:
                    try:
                        create_response(get_message(client), client, messages)
                    except:
                        logger.info(f'Client {client.getpeername()} disconnected')
                        clients.remove(client)
            
            if messages and send_lst:
                for client in send_lst:
                    try:
                        send_message(client, messages[0])
                    except:
                        logger.info(f'Client {client.getpeername()} disconnected')
                        clients.remove(client)
                del messages[0]
    finally:
        s.close()
        logger.info('Server was stopped')


if __name__ == '__main__':
    main()
