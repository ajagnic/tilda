import time
import copy
import os
import json
from blockchain.block import Block

__version__ = '0.0.2'
__author__ = 'Adrian Agnic'

class Blockchain:
    """ Defines the blockchain and its methods """

    def __init__(self):
        self.__set_difficulty(5)
        self.__genesis()

    def __genesis(self):
        """ Initialize the blockchain with the only valid first block """
        self.chain = [Block(self.__proof_of_work({'data': 'Genesis', 'index':0, 'nonce':0, 'prev_hash':0, 'destination':0, 'origin':0, 'timestamp':time.time()}))]

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

    def __set_difficulty(self, num):
        """ Create immutable property of blockchain POW difficulty
        """
        self.__difficulty = (num,)

    def _save_local(self):# NOTE PICKLE
        """ Locally store blockchain as file """
        res = os.listdir()
        if '.chaindata' in res:
            doc = open('.chaindata/.data.txt', 'w')
            for i in range(0, len(self.chain)):
                doc.write(json.dumps(self.chain[i]._properties))
            doc.close()
        else:
            os.mkdir('.chaindata')
            new_doc = open('.chaindata/.data.txt', 'w')
            for i in range(0, len(self.chain)):
                new_doc.write(json.dumps(self.chain[i]._properties))
            new_doc.close()

    def _load_local(self):
        pass

    def get_latest_block(self):
        """ Returns last Block obj in chain """
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data, origin, destination):
        """ Add new block to chain, calculating hash and verifying
        :param data: data of new block
        :type data: dict, str, int, list
        :param origin: origin of block data
        :type origin: str
        :param destination: destination of block data
        :type destination: str
        """
        if type(data) not in [str, int, list, dict]: return False
        if all(isinstance(i, str) for i in [origin, destination]): return False
        prev_block = self.get_latest_block()
        prev_props = prev_block.get_properties()
        block = {
            'data': data,
            'index': (prev_props[1] + 1),
            'nonce':0,
            'prev_hash': prev_props[7],
            'destination': destination,
            'origin': origin,
            'timestamp': time.time()
        }
        self.chain.append(Block(self.__proof_of_work(copy.deepcopy(block))))
        success, res = self.validate_chain()
        if success is True:
            return True, self.chain[len(self.chain)-1]._properties['hash']
        return res

    def validate_chain(self):
        """ Loop through chain, verifying index, hash, and previous hash values """
        res = self.__validate_gen(self.chain[0]._properties, self.chain[0].get_properties())
        if res is False:
            self.__revert_to_valid_block()
            return False, 'Invalid genesis'
        for i in range(1, len(self.chain)):
            props = copy.deepcopy(self.chain[i]._properties)
            prev_props = copy.deepcopy(self.chain[i - 1]._properties)
            # check types
            if self.__validate_types(props) is False:
                self.__revert_to_valid_block()
                return False, 'Invalid data type'
            # check index increment
            elif props['index'] != (prev_props['index'] + 1):
                self.__revert_to_valid_block()
                return False, 'Invalid index'
            # check prev_hash == prev_block.hash
            elif props['prev_hash'] != prev_props['hash']:
                self.__revert_to_valid_block()
                return False, 'Invalid previous hash'
            # check hash == sha(Block data)
            elif self.__validate_blocks_hash(props) is False:
                self.__revert_to_valid_block()
                return False, 'Invalid hash or nonce'
            # check immutable hash values
            elif self.__hard_hash_check(self.chain[i].get_properties(), self.chain[i-1].get_properties()) is False:
                self.__revert_to_valid_block()
                return False, 'Invalid hash'
        return True, 'Success'

    def __hard_hash_check(self, set_props, prev_set_props):
        """ validate_chain helper: check immutable hash values """
        if len(set_props) == len(prev_set_props):
            if set_props[3] == prev_set_props[7]:
                return True
        return False

    def __validate_blocks_hash(self, properties):#NOTE TODO REFACTOR FOR BOTH _props & __props
        """ validate_chain helper: check contents = hash and proof of work used """
        props_copy = copy.deepcopy(properties)
        del props_copy['hash']
        hashed = Block.sha(props_copy)
        if properties['hash'] == hashed:
            if hashed[0:self.__difficulty[0]] == '0' * self.__difficulty[0]:
                return True
        return False

    # def __validate_types(self, properties):# NOTE TODO REFACTOR
    #     """ validate_chain helper: check data types of Block """
    #     if len(properties) == 8:
    #         if isinstance(properties['timestamp'], float):
    #             if all(isinstance(properties['data'], k) for k in [str, int, list, dict]):
    #                 if all(isinstance(j, int) for j in [properties['nonce'], properties['index']]):
    #                     if all(isinstance(i, str) for i in [properties['prev_hash'], properties['hash'], properties['destination'], properties['origin']]):
    #                         return True
    #     return False

    def __validate_gen(self, properties, set_hash):
        if all(x == 0 for x in [properties['index'], properties['prev_hash'], properties['origin'], properties['destination']]):
            if properties['data'] == 'Genesis':
                props_c = copy.deepcopy(properties)
                del props_c['hash']
                hashed = Block.sha(props_c)
                if all(j == hashed for j in [properties['hash'], set_hash[7]])
                    return True
        return False
