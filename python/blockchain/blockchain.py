import time
import copy
import os
import json
from blockchain.block import Block

__version__ = '0.0.5'
__author__ = 'Adrian Agnic'


class Blockchain:

    def __init__(self):
        self.__set_difficulty(6)
        self.load_local()

    def __genesis(self):
        self.chain = [Block(self.__proof_of_work({'data': 'Genesis', 'index': 0, 'nonce': 0, 'prev_hash': 0, 'destination': 0, 'origin': 0, 'timestamp': time.time()}))]

    def __revert(self, index=0):
        del self.chain[index:]
        if len(self.chain) == 0:
            self.__genesis()
        print('!!REVERTED!!')
        success, res = self.validate_chain()
        if success is True:
            self.save_local()
        return res

    def __proof_of_work(self, dictionary):
        """
        Increment a property 'nonce' until the resulting hash has a leading amount of zeros equal to Blockchain.__difficulty
        """
        hashed = Block.sha(dictionary)
        while hashed[:self.__difficulty[0]] != '0' * self.__difficulty[0]:
            dictionary['nonce'] += 1
            hashed = Block.sha(dictionary)
        return dictionary

    def __set_difficulty(self, num):
        self.__difficulty = (num,)

    def save_local(self):
        res = os.listdir()
        if '.chaindata' in res:
            with open('.chaindata/.data.txt', 'w') as doc:
                json.dump([obj.__dict__['_properties'] for obj in self.chain], doc, ensure_ascii=True, indent=4)#, separators=(',', ':'))
            doc.close()
        else:
            os.mkdir('.chaindata')
            with open('.chaindata/.data.txt', 'w') as new_doc:
                json.dump([obj.__dict__['_properties'] for obj in self.chain], new_doc, ensure_ascii=True, indent=4)#, separators=(',', ':'))
            new_doc.close()

    def load_local(self):
        res = os.listdir()
        if '.chaindata' in res:
            with open('.chaindata/.data.txt', 'r') as doc:
                chain_data = json.load(doc)
            doc.close()
            for obj in chain_data:
                del obj['hash']
            self.chain = [Block(x) for x in chain_data]
            return self.validate_chain()
        else:
            self.__genesis()
            self.save_local()

    def get_latest_block(self):
        return self.chain[(len(self.chain) - 1)]

    def add_new_block(self, data, origin, destination):
        if not isinstance(data, (str, int, list, dict)):
            return False
        if not all(isinstance(i, str) for i in [origin, destination]):
            return False
        prev_block = self.get_latest_block()
        prev_props = prev_block.get_properties()
        block = {
            'data': data,
            'index': (prev_props[1] + 1),
            'nonce': 0,
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
            self.__genesis()
            return False, 'Invalid genesis'
        for i in range(1, len(self.chain)):
            try:
                props = copy.deepcopy(self.chain[i]._properties)
                prev_props = copy.deepcopy(self.chain[i - 1]._properties)
            except AttributeError:
                self.__revert(i)
                return False, 'Invalid Block object'
            if props['index'] != (prev_props['index'] + 1):
                self.__revert(i)
                return False, 'Invalid index'
            elif props['prev_hash'] != prev_props['hash']:
                self.__revert(i)
                return False, 'Invalid previous hash'
            elif self.__hash_check(props, self.chain[i].get_properties(), self.chain[i-1].get_properties()) is False:
                self.__revert(i)
                return False, 'Invalid hash'
        return True, 'Success'

    def __hash_check(self, props, iprops, prev_iprops):
        """
        Incorrect Blocks are initialized as empty dicts, check lengths to detect that
        Check property:'prev_hash' equals property:'hash' of previous Block
        Verify hash of all properties equals the property:'hash' value
        Check resulting hash has a leading amount of zeros equal to Blockchain.__difficulty (check if proof of work was used)
        """
        if len(iprops) == len(prev_iprops):
            if iprops[3] == prev_iprops[7]:
                props_c = copy.deepcopy(props)
                hashed = Block.sha(props_c)
                if all(x == hashed for x in [props['hash'], iprops[7]]):
                    if hashed[:self.__difficulty[0]] == '0' * self.__difficulty[0]:
                        return True
        return False

    def __validate_gen(self, properties, set_hash):
        if all(x == 0 for x in [properties['index'], properties['prev_hash'], properties['origin'], properties['destination']]):
            if properties['data'] == 'Genesis':
                props_c = copy.deepcopy(properties)
                hashed = Block.sha(props_c)
                if all(j == hashed for j in [properties['hash'], set_hash[7]]):
                    if hashed[:self.__difficulty[0]] == '0' * self.__difficulty[0]:
                        return True
        return False
