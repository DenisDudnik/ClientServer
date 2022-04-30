from socket import socket, AF_INET, SOCK_STREAM
from shared.const import ENCODING, DEFAULT_PORT, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH


def main():
    s = socket(AF_INET, SOCK_STREAM)
    server_address = ('', DEFAULT_PORT)
    try:
        s.bind(server_address)
        print('Старт сервера на IP "{}" порт "{}"'.format(*server_address))
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
