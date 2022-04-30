import json
from shared.const import ENCODING, MAX_PACKAGE_LENGTH


def send_message(sock, msg):
    msg_json = json.dumps(msg)
    msg_enc = msg_json.encode(ENCODING)
    sock.send(msg_enc)


def get_message(sock):
    msg_enc = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(msg_enc, bytes):
        msg_json = msg_enc.decode(ENCODING)
        msg = json.loads(msg_json)
        if isinstance(msg, dict):
            return msg
        raise ValueError
    raise ValueError
