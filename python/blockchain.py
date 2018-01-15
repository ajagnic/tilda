""" Contains blockchain class structure """
import time
from block import Block

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self):
        self.__genesis()
        self.__set_difficulty(4)

    def __genesis(self):
        """ Initialize the blockchain with the only valid first block """
        self.chain = []
        genesis_block = Block({'index':0, 'timestamp':time.time(), 'data':{'language': 'python', 'code': """print('Genesis')"""}, 'hash':0, 'prev_hash':0, 'sender':0, 'recipient':0, 'nonce':0})
        self.chain.append(genesis_block)

    def __revert_to_valid_block(self):
        print("REVERTED")
        self.__genesis()# NOTE TEMP

    def __proof_of_work(self, dictionary):
        """
        """
        dictionary['nonce'] = 0
        hashed = Block.sha(dictionary)
        while hashed[0:self.__difficulty[0]] != '0' * self.__difficulty[0]:
            dictionary['nonce'] += 1
            hashed = Block.sha(dictionary)
        return dictionary

    def __set_difficulty(self, difficulty):
        """ Create immutable property of blockchain POW difficulty
        :param difficulty: amount of zeros required in hash
        :type difficulty: int
        """
        self.__difficulty = (difficulty,)

    def _save_local(self):
        """ Locally store blockchain as file """
        pass

    def get_latest_block(self):
        """ Returns last Block obj in chain """
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data, sender, recipient):
        """ Add new block to chain, calculating hash and verifying
        :param data: data of new block
        :type data: dict, str, int
        :param sender: origin of block data
        :type sender: str
        :param recipient: destination of block data
        :type recipient: str
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
        proofed_block = self.__proof_of_work(block)
        new_block = Block(proofed_block)
        self.chain.append(new_block)
        self.validate_chain()

    def validate_chain(self):
        """ Loop through chain, verifying index, hash, and previous hash values """
        pass

    def update(self):
        pass
