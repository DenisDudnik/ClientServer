import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from utils.const import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, PRESENCE, \
    TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT
from utils.func import get_message, send_message


def create_presence(account_name='guest', status=''):
    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        "type": "status",
        USER: {
            ACCOUNT_NAME: account_name,
            "status": status
        }
    }
    return msg


def process_answer(msg: dict):
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
        print("Server address wasn't found. Using default address")
        server_address = DEFAULT_IP_ADDRESS

    try:
        server_port = int(sys.argv[2])
    except IndexError:
        print("Server port wasn't found. Using default port")
        server_port = DEFAULT_PORT

    # init socket, connect, send message, get answer
    s = socket(AF_INET, SOCK_STREAM)
    try:
        print(f'Connecting to {server_address}:{server_port}')
        s.connect((server_address, server_port))
    except Exception as e:
        print('Connection failed. Error: ', e)
    else:
        msg = create_presence(account_name='client1', status='I am here!')
        send_message(s, msg)
        try:
            data = get_message(s)
            print('From server: ', process_answer(data))
        except (ValueError, json.JSONDecodeError):
            print('Unknown message from server')
    finally:
        s.close()


if __name__ == '__main__':
    main()
