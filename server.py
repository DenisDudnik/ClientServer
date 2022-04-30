import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
from shared.const import ENCODING, DEFAULT_PORT, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH


def main():
    "server -p 5555 -a 127.0.0.1"

    "try to find port in args"
    if '-p' in sys.argv:
        try:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
        except IndexError:
            print('After -p should be port number')
            sys.exit(1)
        except ValueError:
            print('Port should be a number in 1024..65535')
            sys.exit(1)
    else:
        server_port = DEFAULT_PORT

    "try to find address in args"
    if '-a' in sys.argv:
        try:
            server_address = sys.argv[sys.argv.index('-a') + 1]
        except IndexError:
            print('After -a should be address to listen')
            sys.exit(1)
    else:
        server_address = ''

    s = socket(AF_INET, SOCK_STREAM)
    server_address_pair = (server_address, server_port)
    try:
        s.bind(server_address_pair)
        print('Старт сервера на IP "{}" порт "{}"'.format(*server_address_pair))
    except OSError as e:
        print('Error open socket. Error: ', e)
    else:
        s.listen(MAX_CONNECTIONS)

        while True:
            client, addr = s.accept()
            data = client.recv(MAX_PACKAGE_LENGTH)
            print('From:', addr, ' =>', data.decode(ENCODING))

            msg = 'Привет'
            client.send(msg.encode(ENCODING))
            client.close
    finally:
        s.close()


if __name__ == '__main__':
    main()
