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
        return self.validate_chain()

    def validate_chain(self):
        """ Loop through chain, verifying index, hash, and previous hash values """
        for i in range(1, (len(self.chain) - 1)):
            cur_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if cur_block.__properties[0] != (prev_block.__properties[0] + 1):
                self.__revert_to_valid_block()
                return False
            if cur_block.__properties[3] != Block.sha(cur_block._properties):
                self.__revert_to_valid_block()
                return False
            if cur_block.__properties[4] != prev_block.__properties[3]:
                self.__revert_to_valid_block()
                return False
            if cur_block.__properties[4] != Block.sha(prev_block._properties):
                self.__revert_to_valid_block()
                return False
        return True

    def __revert_to_valid_block(self):
        self.__genesis()# NOTE TEMP

    def update(self):
        pass
