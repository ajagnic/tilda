""" Contains blockchain class structure """
import time
import copy
from block import Block

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self, difficulty):
        self.__set_difficulty(difficulty)
        self.__genesis()

    def __genesis(self):
        """ Initialize the blockchain with the only valid first block """
        self.chain = []
        proofed_gen_dict = self.__proof_of_work(self.__generate_gen_dict())
        genesis_block = Block(proofed_gen_dict)
        self.chain.append(genesis_block)

    def __generate_gen_dict(self):
        return {'data':{'language': 'python', 'code': """print('Genesis')"""}, 'index':0, 'nonce':0, 'prev_hash':0, 'recipient':0, 'sender':0, 'timestamp':time.time()}

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
        :type data: dict, str, int, list
        :param sender: origin of block data
        :type sender: str
        :param recipient: destination of block data
        :type recipient: str
        """
        allowed = [str, int, list, dict]
        if type(data) not in allowed:
            return None
        elif type(sender) and type(recipient) != str:
            return None
        prev_block = self.get_latest_block()
        prev_props = prev_block.get_properties()
        block = {
            'data': data,
            'index': (prev_props[1] + 1),
            'nonce':0,
            'prev_hash': prev_props[7],
            'recipient': recipient,
            'sender': sender,
            'timestamp': time.time()
        }
        proofed_block = self.__proof_of_work(block)
        valid_block = Block(proofed_block)
        self.chain.append(valid_block)
        if self.validate_chain():
            return True

    def validate_chain(self):
        """ Loop through chain, verifying index, hash, and previous hash values """
        for i in range(1, len(self.chain)):
            props = self.chain[i]._properties
            prev_props = self.chain[i - 1]._properties
            # check index increment
            if props['index'] != (prev_props['index'] + 1):
                self.__revert_to_valid_block()
                print('Invalid index found')
                return False
            # check prev_hash == prev_block.hash
            elif props['prev_hash'] != prev_props['hash']:
                self.__revert_to_valid_block()
                print('Invalid previous hash found')
                return False
            # check hash == sha(Block data)
            elif self.__validate_blocks_hash(props) is False:# BUG
                self.__revert_to_valid_block()
                print('Invalid hash or nonce found')
                return False
            else:
                return True

    def __validate_blocks_hash(self, properties):
        """ validate_chain helper """
        props_copy = copy.deepcopy(properties)
        del props_copy['hash']
        hashed = Block.sha(props_copy)
        if properties['hash'] == hashed:
            if hashed[0:self.__difficulty[0]] == '0' * self.__difficulty[0]:
                return True
            else:
                return False
        else:
            return False
