import argparse
import json
import sys
import time
import logging
import threading
import log.config.client_log_config
from socket import socket, AF_INET, SOCK_STREAM
from decors import Log
from utils import const
from utils.func import get_message, send_message

logger = logging.getLogger('app.client')

@Log()
def show_help():
    print("""
    Available commands:\n
    !help - show this help message\n
    !exit - exit the application\n
    !send - send a message\n
    after this command you will be asked for recipient and message\n
    """)

@Log()
def create_presence(account_name, status=''):
    '''Function create presence message'''
    msg = {
        const.ACTION: const.PRESENCE,
        const.TIME: time.time(),
        "type": "status",
        const.USER: {
            const.ACCOUNT_NAME: account_name,
            "status": status
        }
    }
    logger.debug(f'Create presence message: {msg}')
    return msg


@Log()
def create_exit():
    '''Function create exit message'''
    msg = {
        const.ACTION: const.EXIT,
    }
    logger.debug(f'Create exit message: {msg}')
    return msg

@Log()
def create_message(account_name):
    '''Function get user's text and recipient and create message
    '''
    
    to = input("Enter recipient's name: ")
    message = input("Enter message: ")
    
    # create message
    msg = {
        const.ACTION: const.MESSAGE,
        const.TIME: time.time(),
        const.FROM: account_name,
        const.TO: to,
        const.MESSAGE_TEXT: message,
    }
    logger.debug(f'Create message: {msg}')
    return msg

@Log()
def query_message_from_user(sock, account_name):
    '''Function get user's command and create message
    or finish work
    '''
    show_help()
    while True:
        print("Enter command")
        command = input()
        if command == '!exit':
            send_message(sock, create_exit())
            logger.info("Client closed by user's command")
            print("Good bye")
            time.sleep(0.5)
            sock.close()
            break
        elif command == '!send':
            try:
                send_message(sock, create_message(account_name))
                print("Message was sent")
            except:
                logger.critical("Connection was lost")
                break
        elif command == '!help':
            show_help()
        else:
            print(f"Unknown command: {command}")
            show_help()

    return

@Log()
def process_answer(s:socket, account_name):
    '''Function process answer message'''
    while True:
        try:
            msg = get_message(s)
            logger.debug(f'From server: {msg}')
        except (ValueError, json.JSONDecodeError):
            logger.warning(f'Unknown message from server: {msg}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            logger.critical("Connection was lost")
            break
        else:
            logger.debug(f'Process message: {msg}')
    
            # response messages
            if const.RESPONSE in msg:
                # for 2xx messages
                if msg[const.RESPONSE] in range(200, 300):
                    logger.debug(f'{msg[const.RESPONSE]}: {msg.get(const.ALERT)}')
                    print(f"Welcome, {account_name}")
                # for other messages
                logger.debug(f'{msg[const.RESPONSE]}: {msg.get(const.ERROR)}')
                # Maybe username is busy
                print(f"Error: {msg.get(const.ERROR)}")

            # action messages
            elif const.ACTION in msg:
                # text messages
                if msg[const.ACTION] == const.MESSAGE and const.TIME in msg\
                    and const.FROM in msg and const.MESSAGE_TEXT in msg \
                        and const.TO in msg:
                    # message for this user
                    if msg.get(const.TO) == account_name:
                        print(f"FROM {msg.get(const.FROM)}: {msg.get(const.MESSAGE_TEXT)}")
                    # message for other or chat
                    else:
                        pass
            
            # unknown message type
            else: 
                logger.error(f'Incorrect message: {msg}')

    


@Log()
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_address", help="server address", default=const.DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument("server_port", type=int, help="server port", default=const.DEFAULT_PORT, nargs="?")
    parser.add_argument("-n", "--name", help="user name", default=None, nargs="?")
    args = parser.parse_args()

    server_address = args.server_address
    server_port = args.server_port
    account_name = args.name

    if server_port < 1024 or server_port > 65535:
        logger.critical(f'Port should be in range 1024 to 65535. Port given is {server_port}')
        sys.exit(1)
       
    return server_address, server_port, account_name


def main():
    # client 127.0.0.1 5555 -n username

    print("Welcome on the best messanger!!!")
    server_address, server_port, account_name = get_args()

    if not account_name:
        account_name = input("Please enter your account name: ")
    
    # if user entered empty username
    if not account_name:
        logger.critical("User didn't enter username")
        sys.exit(1)
    
    logger.info(
        f"Client running. Server address: {server_address}. "
        f"Port: {server_port}. Account name: {account_name}")

    # init socket, connect, send presence
    s = socket(AF_INET, SOCK_STREAM)
    try:
        logger.info(f'Connecting to {server_address}:{server_port}')
        s.connect((server_address, server_port))
        msg = create_presence(account_name=account_name, status='I am here!')
        send_message(s, msg)
        try:
            data = get_message(s)
            logger.debug(f'From server: {data}')
            print(f"{account_name} was connected to {server_address}:{server_port}")
        except (ValueError, json.JSONDecodeError):
            logger.warning('Unknown message from server')
    except Exception as e:
        logger.critical(f'Connection failed. Error: {e}')
    else:
        # work mode
        income_service = threading.Thread(target=process_answer, args=(s, account_name))
        income_service.daemon = True
        income_service.start()

        send_service = threading.Thread(target=query_message_from_user, args=(s, account_name))
        send_service.daemon = True
        send_service.start()

        logger.debug('Services started')

        while income_service.is_alive() and send_service.is_alive():
            time.sleep(1)
    
    input('Press any key')



if __name__ == '__main__':
    main()
