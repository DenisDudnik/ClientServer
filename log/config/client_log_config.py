import logging
import os
import sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(path)

from utils.const import ENCODING, LOG_LEVEL

logger = logging.getLogger('app.client')

formatter = logging.Formatter('%(asctime)-24s %(levelname)-8s %(module)-15s %(message)s')

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'client.log')
fh = logging.FileHandler(filename, encoding=ENCODING)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(LOG_LEVEL)


if __name__ == '__main__':
    logger.critical('Critical')
    logger.error('Error')
    logger.warning('Warning')
    logger.info('Starting')
    logger.debug('Debug')

