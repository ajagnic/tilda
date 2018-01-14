""" Contains blockchain class structure """
import time
from block import Block

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self):
        self.chain = []

    def __genesis(self):
        genesis_block = Block({'index':0, 'timestamp':time.time(), 'data':'Genesis Block', 'hash':0, 'prev_hash':0})
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data):
        prev_block = self.get_latest_block()
        prev_props = prev_block.get_properties()
        block = {
            'index':(prev_props[0] + 1),
            'timestamp':time.time(),
            'data': data,
            'hash':0,
            'prev_hash':prev_props[3]
        }
        block_obj = Block(block)
        self.chain.append(block_obj)

    def validate_chain(self):
        pass

if __name__ == '__main__':
    bc = Blockchain()
    bc.__genesis()
    blok = bc.get_latest_block()
    print(blok.get_properties())
