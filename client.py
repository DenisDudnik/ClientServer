import json
import sys
from socket import socket, AF_INET, SOCK_STREAM
from shared.const import ENCODING, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_PACKAGE_LENGTH


def main():
    # client 127.0.0.1 5555

    # try to find server address and port in args
    try:
        server_address = sys.argv[1]
    except IndexError:
        print("Server address wasn't found. Using default address")
        server_address = DEFAULT_IP_ADDRESS

    try:
        server_port = sys.argv[2]
    except IndexError:
        print("Server port wasn't found. Using default port")
        server_port = DEFAULT_PORT

    s = socket(AF_INET, SOCK_STREAM)
    try:
        print(f'Connecting to {server_address}:{server_port}')
        s.connect((server_address, server_port))
    except Exception as e:
        print('Connection failed. Error: ', e)
    else:
        msg = 'Серверу КУ'
        s.send(msg.encode(ENCODING))
        data = s.recv(MAX_PACKAGE_LENGTH)
        print('From server: ', data.decode(ENCODING))
    finally:
        s.close()


if __name__ == '__main__':
    main()
