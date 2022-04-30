from socket import socket, AF_INET, SOCK_STREAM
from shared.const import ENCODING, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_PACKAGE_LENGTH

s = socket(AF_INET, SOCK_STREAM)
try:
    s.connect((DEFAULT_IP_ADDRESS, DEFAULT_PORT))
except ConnectionRefusedError as e:
    print('Server unavailable. Error: ', e)
else:
    msg = 'Серверу КУ'
    s.send(msg.encode(ENCODING))
    data = s.recv(MAX_PACKAGE_LENGTH)
    print('From server: ', data.decode(ENCODING))
finally:
    s.close()
