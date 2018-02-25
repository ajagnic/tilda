import time
import hashlib

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Tilde:
    """ storage interface class """

    def __init__(self, filepath):
        pass

    def save(self, data):
        """ add new block """
        pass

    def commit(self):
        """ mine and store """
        pass



class Blockchain:

    def __init__(self):
        pass

    def add(self, data):
        pass



class Block:

    def __init__(self, data, prev_block):
        self.__dict__ = self.create(data, prev_block)

    def create(self, data, prev_block):
        """
        :data: any allowed in dict
        :prev_block: dict
        :return: dict
        """
        prev_index, prev_hash = prev_block["head"]["index"], prev_block["head"]["hash"]
        block = {
            "body": {
                "meta": {
                    "index": prev_index + 1,
                    "time": time.time(),
                    "prevHash": prev_hash,
                    "nonce": None
                },
                "data": data
            }
        }
        return block

    def hash(self, block):
        pass
