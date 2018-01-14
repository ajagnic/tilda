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
        genesis_block = Block({'index':0, 'timestamp':time.time(), 'data':{'language': 'python', 'code': """print('Genesis')"""}, 'hash':0, 'prev_hash':0, 'sender':0, 'recipient':0, 'nonce':0})
        self.chain.append(genesis_block)
        self.add_new_block('buffer', 0, 0)# NOTE TODO FIX VALIDATION STARTING ON 1st INDEX

    def __revert_to_valid_block(self):
        print("REVERTED")
        self.__genesis()# NOTE TEMP

    def __proof_of_work(self):
        pass

    def _save_local(self):
        """ Locally store blockchain as file """
        pass

    def get_latest_block(self):
        """ Returns last Block obj in chain """
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data, sender, recipient):# NOTE TODO ADD PROOF OF WORK
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
            'prev_hash': prev_props[3],
            'sender': sender,
            'recipient': recipient,
            'nonce':0
        }
        new_block = Block(block)
        self.chain.append(new_block)
        self.validate_chain()

    def validate_chain(self):# NOTE TODO REFACTOR
        """ Loop through chain, verifying index, hash, and previous hash values """
        for i in range(1, (len(self.chain) - 1)):
            cur_block = self.chain[i]
            prev_block = self.chain[i - 1]
            try:
                cur_props = cur_block.get_properties()
                prev_props = prev_block.get_properties()
            except AttributeError:
                self.__revert_to_valid_block()
            else:
                print(i)
                if len(cur_block._properties) == 0:
                    self.__revert_to_valid_block()
                if cur_props[0] != (prev_props[0] + 1):
                    self.__revert_to_valid_block()
                if cur_props[3] != Block.sha(cur_block._properties):
                    self.__revert_to_valid_block()
                if cur_props[4] != prev_props[3]:
                    self.__revert_to_valid_block()
                if cur_props[4] != Block.sha(prev_block._properties):
                    self.__revert_to_valid_block()
        return True

    def update(self):
        pass
