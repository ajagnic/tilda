""" Contains blockchain class structure """
import time
from block import Block

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self):
        self.__set_difficulty(4)
        self.__genesis()

    def __genesis(self):
        """ Initialize the blockchain with the only valid first block """
        self.chain = []
        proofed_gen_dict = self.__proof_of_work(self.__generate_gen_dict())
        genesis_block = Block(proofed_gen_dict)
        self.chain.append(genesis_block)

    def __generate_gen_dict(self):
        return {'index':0, 'timestamp':time.time(), 'data':{'language': 'python', 'code': """print('Genesis')"""}, 'prev_hash':0, 'sender':0, 'recipient':0, 'nonce':0}

    def __revert_to_valid_block(self):
        print("REVERTED")
        self.__genesis()# NOTE TEMP

    def __proof_of_work(self, dictionary):
        """ Calculate a nonce value that results in a Block hash with an amount of leading zeros equal to difficulty
        :param dictionary: Block properties
        :type dictionary: dict
        """
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
        :type data: dict, str, int, arr
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
            'prev_hash': prev_props[3],
            'sender': sender,
            'recipient': recipient,
            'nonce':0
        }
        proofed_block = self.__proof_of_work(block)
        valid_block = Block(proofed_block)
        self.chain.append(valid_block)
        self.validate_chain()

    def validate_chain(self):
        """ Loop through chain, verifying index, hash, and previous hash values
        """
        for i in range(0, len(self.chain)):
            if i == 0:
                if self.comparator(self.chain[0], self.__generate_gen_dict()):
                    pass
                else:
                    self.__revert_to_valid_block()
            elif i > 0 and i < len(self.chain):
                if self.validate_block(self.chain[i], self.chain[i - 1]):
                    pass
                else:
                    self.__revert_to_valid_block()
            else:
                self.__revert_to_valid_block()


    @staticmethod
    def comparator(block_a, block_b):
        """ Compare values of two Blocks, return true if equal
        :type block_a: Block obj
        :type block_b: Block obj
        """
        a_props = block_a.get_properties()
        b_props = block_b.get_properties()
        if len(a_props) != len(b_props):
            return False
        for i in range(0, len(a_props)):
            if a_props[i] != b_props[i]:
                return False
        return True

    @staticmethod
    def validate_block(cur_block, prev_block):
        """ Validate values of a block addition, return true if correct
        :type cur_block: Block obj
        :type prev_block: Block obj
        """
        cur_props = cur_block.get_properties()
        prev_props = prev_block.get_properties()
        if cur_props[0] != (prev_props[0] + 1):
            return False
        elif cur_props[3] != prev_props[6]:
            return False
        else:
            return True
