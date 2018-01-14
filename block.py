""" Contains class structure of a single block """
import hashlib

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Block:
    """ Defines a block and its methods """

    def __init__(self, dictionary):
        """
        :param dictionary: only containing fields listed in get_accepted_keys()
        :type dictionary: dict
        """
        self.__set_accepted_keys()
        self.__set_properties(dictionary)

    def __set_accepted_keys(self):
        # accepted keys are stored as a tuple to avoid re-assignment
        self.__accepted_keys = ('index', 'timestamp', 'data', 'hash', 'prev_hash')

    def get_accepted_keys(self):
        """ Return list of accepted keys to use for initializing a Block """
        return self.__accepted_keys

    def __set_properties(self, dictionary):
        self._properties = {}
        if len(dictionary) == len(self.get_accepted_keys()):
            for key, value in dictionary.items():
                if key in self.get_accepted_keys():
                    self._properties[key] = value
                else:
                    self._properties = {}
                    return None

    @staticmethod
    def hash(index, timestamp, data, hsh, prev_hash):
        """ Method that accepts fields of a Block, returns hash of all fields
        :type index: int
        :type timestamp: int
        :type data: multiple types allowed *NOTE TODO*
        :type hsh: str
        :type prev_hash: str
        """
        cat = str(index) + str(timestamp) + str(data) + str(hsh) + str(prev_hash)
        hashed = hashlib.sha256(cat.encode()).hexdigest()
        return hashed
