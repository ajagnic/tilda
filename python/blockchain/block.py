import hashlib

__version__ = '0.0.5'
__author__ = 'Adrian Agnic'

class Block:

    def __init__(self, dictionary):
        self.__accepted_keys = ('data', 'index', 'nonce', 'prev_hash', 'destination', 'origin', 'timestamp')
        if isinstance(dictionary, dict): self.__set_attr(dictionary)

    def __repr__(self):
        return "Index: {},\n Hash: {},\n PreviousHash: {},\n Timestamp: {}\n".format(self._properties['index'], self._properties['hash'], self._properties['prev_hash'], self._properties['timestamp'])

    def __set_attr(self, dictionary):
        """
        Store input dict as Block._properties
        Hash values of Block._properties and assign to new key: 'hash'
        Store Block._properties values as immutable tuple: Block.__properties
        """
        if self.verify(dictionary) is False: return None
        self._properties = {key: value for key, value in dictionary.items()}
        self._properties['hash'] = self.sha(self._properties)
        self.__properties = (self._properties['data'], self._properties['index'], self._properties['nonce'], self._properties['prev_hash'], self._properties['destination'], self._properties['origin'], self._properties['timestamp'], self._properties['hash'])

    def get_accepted_keys(self):
        return self.__accepted_keys

    def get_properties(self):
        return self.__properties

    def verify(self, dictionary):
        """
        Verify input dict and Block.__accepted_keys have same amount of keys, and the key names are equal
        """
        if isinstance(dictionary, dict):
            if len(dictionary) == len(self.get_accepted_keys()):
                for k, v in dictionary.items():
                    if k in self.get_accepted_keys():
                        pass
                    else:
                        return False
                return True
        return False

    @staticmethod
    def sha(properties):
        cat = "{0}{1}{2}{3}{4}{5}{6}".format(properties['data'], properties['index'], properties['nonce'], properties['prev_hash'], properties['destination'], properties['origin'], properties['timestamp'])
        hashed = hashlib.sha256(cat.encode()).hexdigest()
        return hashed
