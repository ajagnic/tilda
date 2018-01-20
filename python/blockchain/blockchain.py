""" Contains blockchain class structure, properties and methods are terribly abstracted """
import time
import copy
from blockchain.block import Block

__version__ = '0.0.2'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self):
        self.__set_difficulty()
        self.__genesis()

    def __genesis(self):
        """ Initialize the blockchain with the only valid first block """
        self.chain: list = [Block(self.__proof_of_work({'data': 'Genesis', 'index':0, 'nonce':0, 'prev_hash':0, 'recipient':0, 'sender':0, 'timestamp':time.time()}))]

    def __revert_to_valid_block(self):
        print('REVERTED')
        self.__genesis()

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

    def __set_difficulty(self):
        """ Create immutable property of blockchain POW difficulty
        """
        self.__difficulty: tuple = (5,)

    def _save_local(self):
        """ Locally store blockchain as file """
        pass # NOTE TODO

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
        if type(data) not in [str, int, list, dict]: return False
        if type(sender) and type(recipient) is not str: return False
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
        self.chain.append(Block(self.__proof_of_work(copy.deepcopy(block))))
        res: [tuple, bool] = self.validate_chain()
        if res[0] is True:
            return (True, self.chain[len(self.chain)-1]._properties['hash'])
        return res

    def validate_chain(self):
        """ Loop through chain, verifying index, hash, and previous hash values """
        for i in range(1, len(self.chain)):
            props: dict = copy.deepcopy(self.chain[i]._properties)
            prev_props: dict = copy.deepcopy(self.chain[i - 1]._properties)
            # check types
            if self.__validate_types(props) is False:
                self.__revert_to_valid_block()
                return (False, 'Invalid data type')
            # check index increment
            elif props['index'] != (prev_props['index'] + 1):
                self.__revert_to_valid_block()
                return (False, 'Invalid index')
            # check prev_hash == prev_block.hash
            elif props['prev_hash'] != prev_props['hash']:
                self.__revert_to_valid_block()
                return (False, 'Invalid previous hash')
            # check hash == sha(Block data) MAIN CHECK
            elif self.__validate_blocks_hash(props) is False:
                self.__revert_to_valid_block()
                return (False, 'Invalid hash or nonce')
            # check timestamp
            elif props['timestamp'] < prev_props['timestamp']:
                self.__revert_to_valid_block()
                return (False, 'Invalid timestamp')
            # check immutable hash values
            elif self.__hard_hash_check(self.chain[i].get_properties(), self.chain[i-1].get_properties()) is False:
                self.__revert_to_valid_block()
                return (False, 'Invalid hash')
        return (True, 'Success')

    def __hard_hash_check(self, set_props, prev_set_props):
        """ validate_chain helper: check immutable hash values """
        if len(set_props) == len(prev_set_props):
            if set_props[3] == prev_set_props[7]:
                return True
            return False
        return False

    def __validate_blocks_hash(self, properties):
        """ validate_chain helper: check contents = hash and proof of work used """
        props_copy: dict = copy.deepcopy(properties)
        del props_copy['hash']
        hashed = Block.sha(props_copy)
        if properties['hash'] == hashed:
            if hashed[0:self.__difficulty[0]] == '0' * self.__difficulty[0]:
                return True
            return False
        return False

    def __validate_types(self, properties):
        """ validate_chain helper: check data types of Block """
        if len(properties) == 8:
            if type(properties['data']) in [str, int, list, dict]:
                if type(properties['timestamp']) is float:
                    if type(properties['nonce']) and type(properties['index']) is int:
                        if type(properties['prev_hash']) and type(properties['hash']) and type(properties['recipient']) and type(properties['sender']) is str:
                            return True
        return False

if __name__ == '__main__':
    bc = Blockchain()
    print(bc.chain)
    for i in range(0, 4):
        bc.add_new_block('hello', 'm', 'n')
    print(bc.chain)
