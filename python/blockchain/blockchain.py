import time
import copy
import os
import json
from blockchain.block import Block

__version__ = '0.0.2'
__author__ = 'Adrian Agnic'

class Blockchain:

    def __init__(self):
        self.__set_difficulty(5)
        self.__genesis()

    def __genesis(self):
        self.chain = [Block(self.__proof_of_work({'data': 'Genesis', 'index':0, 'nonce':0, 'prev_hash':0, 'destination':0, 'origin':0, 'timestamp':time.time()}))]

    def __revert_to_valid_block(self):
        print('REVERTED')
        self.__genesis()# NOTE TEMP

    def __proof_of_work(self, dictionary):
        hashed = Block.sha(dictionary)
        while hashed[0:self.__difficulty[0]] != '0' * self.__difficulty[0]:
            dictionary['nonce'] += 1
            hashed = Block.sha(dictionary)
        return dictionary

    def __set_difficulty(self, num):
        self.__difficulty = (num,)

    def _save_local(self):# NOTE PICKLE OR JSON
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
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data, origin, destination):
        if not isinstance(data, (str, int, list, dict)): return False
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
        res = self.__validate_gen(self.chain[0]._properties, self.chain[0].get_properties())
        if res is False:
            self.__revert_to_valid_block()
            return False, 'Invalid genesis'
        for i in range(1, len(self.chain)):
            props = copy.deepcopy(self.chain[i]._properties)
            prev_props = copy.deepcopy(self.chain[i - 1]._properties)
            elif props['index'] != (prev_props['index'] + 1):
                self.__revert_to_valid_block()
                return False, 'Invalid index'
            elif props['prev_hash'] != prev_props['hash']:
                self.__revert_to_valid_block()
                return False, 'Invalid previous hash'
            elif self.__hash_check(props, self.chain[i].get_properties(), self.chain[i-1].get_properties()) is False:
                self.__revert_to_valid_block()
                return False, 'Invalid hash'
        return True, 'Success'

    def __hash_check(self, props, iprops, prev_iprops):
        pass

    # def __hard_hash_check(self, set_props, prev_set_props):
    #     if len(set_props) == len(prev_set_props):
    #         if set_props[3] == prev_set_props[7]:
    #             return True
    #     return False
    #
    # def __validate_blocks_hash(self, properties):#NOTE TODO REFACTOR FOR BOTH _props & __props
    #     props_copy = copy.deepcopy(properties)
    #     hashed = Block.sha(props_copy)
    #     if properties['hash'] == hashed:
    #         if hashed[0:self.__difficulty[0]] == '0' * self.__difficulty[0]:
    #             return True
    #     return False

    def __validate_gen(self, properties, set_hash):
        if all(x == 0 for x in [properties['index'], properties['prev_hash'], properties['origin'], properties['destination']]):
            if properties['data'] == 'Genesis':
                props_c = copy.deepcopy(properties)
                hashed = Block.sha(props_c)
                if all(j == hashed for j in [properties['hash'], set_hash[7]])
                    return True
        return False
