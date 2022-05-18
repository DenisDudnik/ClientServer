import sys
import json
import logging
import log.config.server_log_config
from socket import socket, AF_INET, SOCK_STREAM
from utils.const import ENCODING, DEFAULT_PORT, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT
from utils.func import get_message, send_message

logger = logging.getLogger('server')

def create_response(msg):
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


def main():
    # server -p 5555 -a 127.0.0.1

    # try to find port in args
    if '-p' in sys.argv:
        try:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
        except IndexError:
            logger.error('After -p should be port number')
            sys.exit(1)
        except ValueError:
            logger.error('Port should be a number in 1024..65535')
            sys.exit(1)
    else:
        server_port = DEFAULT_PORT

    # try to find address in args
    if '-a' in sys.argv:
        try:
            server_address = sys.argv[sys.argv.index('-a') + 1]
        except IndexError:
            logger.error('After -a should be address to listen')
            sys.exit(1)
    else:
        server_address = ''

    s = socket(AF_INET, SOCK_STREAM)
    server_address_pair = (server_address, server_port)
    try:
        s.bind(server_address_pair)
        logger.info('Старт сервера на IP "{}" порт "{}"'.format(*server_address_pair))
    except OSError as e:
        logger.error('Error open socket. Error: ', e)
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
