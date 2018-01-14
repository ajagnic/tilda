""" Contains blockchain class structure """
import time

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    genesis = {
        'index': 0,
        'timestamp': time.time(),
        'data': {
            'message': 'Genesis'
        },
        'hash': 0,
        'prev_hash': 0
    }

    def __init__(self, blockchain):
        self.blockchain = blockchain
