""" Contains blockchain class structure """
import time
from block import Block

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self):
        self.__genesis()

    def __genesis(self):
        """ Initialize the blockchain with the only valid first block """
        self.chain = []
        genesis_block = Block({'index':0, 'timestamp':time.time(), 'data':{'language': 'python', 'code': """print('Genesis')"""}, 'hash':0, 'prev_hash':0})
        self.chain.append(genesis_block)

    def get_latest_block(self):
        """ Returns last Block obj in chain """
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data):# NOTE TODO ADD PROOF OF WORK
        """ Add new block to chain, calculating hash and verifying
        :param data: data of new block
        :type data: dict, str, int
        """
        prev_block = self.get_latest_block()
        prev_props = prev_block.get_properties()
        block = {
            'index': (prev_props[0] + 1),
            'timestamp': time.time(),
            'data': data,
            'hash': 0,
            'prev_hash': prev_props[3]
        }
        new_block = Block(block)
        self.chain.append(new_block)
        valid = self.validate_chain()
        if valid is False:
            self.__revert_to_valid_block()

    def validate_chain(self):# NOTE TODO REFACTOR
        for i in range(1, (len(self.chain) - 1)):
            cur_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if cur_block._properties['index'] != (prev_block._properties['index'] + 1):
                return False
            elif cur_block._properties['hash'] != Block.sha(cur_block._properties):
                return False
            elif cur_block._properties['prev_hash'] != prev_block._properties['hash']:
                return False
            elif cur_block._properties['prev_hash'] != Block.sha(prev_block._properties):
                return False
        return True

    def __revert_to_valid_block(self):
        self.chain = []# TEMP

    def update(self):
        pass
