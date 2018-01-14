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

    def __set_properties(self, dictionary):
        self._properties = {}
        if len(dictionary) == len(self.get_accepted_keys()):
            for key, value in dictionary.items():
                if key in self.get_accepted_keys():
                    self._properties[key] = value
                else:
                    self._properties = {}
                    return None
            self._properties['hash'] = self.sha(self._properties)
            # store properties as immmutable
            self.__properties = (self._properties['index'], self._properties['timestamp'], self._properties['data'], self._properties['hash'], self._properties['prev_hash'])

    def get_accepted_keys(self):
        """ Return list of accepted keys to use for initializing a Block """
        return self.__accepted_keys

    def get_properties(self):
        """ Returns tuple of Block instance property values """
        return self.__properties

    def load_program(self):
        pass

    @staticmethod
    def sha(properties):
        """ Method that accepts fields of a Block, returns hash of all fields
        :param properties: properties of a Block instance
        :type properties: dict
        """
        cat = str(properties['index']) + str(properties['timestamp']) + str(properties['data']) + str(properties['prev_hash'])
        hashed = hashlib.sha256(cat.encode()).hexdigest()
        return hashed
