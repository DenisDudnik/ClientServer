import argparse
import json
import logging
import select
import sys
import time
import log.config.server_log_config

from socket import socket, AF_INET, SOCK_STREAM
from decors import Log, log_dec
from utils import const
from utils.func import get_message, send_message

logger = logging.getLogger('app.server')

@log_dec
def create_response(msg:dict, client:socket, message_list:list, users:dict, clients:list):
    '''Function to create a response'''
    logger.debug(f'Process message: {msg}')

    # valid presense message
    if const.ACTION in msg and msg[const.ACTION] == const.PRESENCE and const.TIME in msg and const.USER in msg \
            and msg[const.USER][const.ACCOUNT_NAME]:
        # and msg[USER][ACCOUNT_NAME] in contact_list:
        
        # new user connected?
        if msg.get(const.USER).get(const.ACCOUNT_NAME) not in users.keys():
            users[msg[const.USER][const.ACCOUNT_NAME]] = client
        
        msg = {
            const.RESPONSE: 200,
            const.ALERT: "OK"
        }
        send_message(client, msg)
        logger.info(f'Create and send response: {msg} for user')
        return
    
    # valid quit message
    if const.ACTION in msg and msg[const.ACTION] == const.EXIT and const.ACCOUNT_NAME in msg:
        # and msg[USER][ACCOUNT_NAME] in contact_list:
        msg = {
            const.RESPONSE: 200,
            const.ALERT: "Good bye!"
        }
        send_message(client, msg)
        logger.info(f'Create and send response: {msg} for user')
        time.sleep(0.5)
        client.close()
        clients.pop(msg[const.ACCOUNT_NAME])
        users.pop(msg[const.ACCOUNT_NAME])
        return

    # text messages (we shouldn't process msg, just resend to client or chat)
    if const.ACTION in msg and msg[const.ACTION] == const.MESSAGE and const.TIME in msg \
        and const.FROM in msg and const.TO in msg and const.MESSAGE_TEXT in msg:
            message_list.append(msg)
            logger.info(f'Append message to list: {msg}')
            # TODO: here we should create message for author (response 200)
            return
    
    # bad message
    msg = {
        const.RESPONSE: 400,
        const.ERROR: "Bad Request"
    }

    logger.info(f'Create response: {msg}')
    if client:
        send_message(client, msg)
    return


@log_dec
def send_msg_to_user(msg:dict, users:dict, send_lst:list):
    '''Function to send a message to user'''
    logger.debug(f'Process message: {msg}')

    # text messages (we shouldn't process msg, just resend to client or chat)
    # if const.ACTION in msg and msg[const.ACTION] == const.MESSAGE and const.TIME in msg \
    #     and const.FROM in msg and const.TO in msg and const.MESSAGE_TEXT in msg:
    #         message_list.append(msg)
    #         logger.info(f'Append message to list: {msg}')
    #         # TODO: here we should create message for author (response 200)
    #         return
    
    # user was found in server list and in waiting list
    if msg[const.TO] in users and users[msg[const.TO]] in send_lst:
        send_message(users[msg[const.TO]], msg)
        logger.info(f'Send message. From {msg[const.FROM]} to {msg[const.TO]}: {msg}')
    # user was found in server list but not in waiting list, probably disconnected
    elif msg[const.TO] in users and users[msg[const.TO]] not in send_lst:
        raise ConnectionError
    # user wasn't found
    else:
        logger.info(f"User {msg[const.TO]} wasn't found on server")
    return


@log_dec
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="server address", default="", nargs="?")
    parser.add_argument("-p", "--port", type=int, help="server port", default=const.DEFAULT_PORT, nargs="?")
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
        s.listen(const.MAX_CONNECTIONS)
        logger.info(f'Server was run on {server_address}:{server_port}')
        print(f'Server was run on {server_address or "ANY"}:{server_port}')

        clients, messages = [], []
        users = {}

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
                        create_response(get_message(client), client, messages, users, clients)
                    except:
                        logger.info(f'Client {client.getpeername()} was disconnected')
                        clients.remove(client)
            
            for message in messages:
                try:
                    send_msg_to_user(message, users, send_lst)
                except:
                    logger.info(f'Client {message[const.TO]} was disconnected')
                    clients.remove(users[message[const.TO]])
                    users.pop(message[const.TO])
            messages.clear()

    finally:
        s.close()
        logger.info('Server was stopped')


if __name__ == '__main__':
    main()
