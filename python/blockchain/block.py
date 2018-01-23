import hashlib

__version__ = '0.0.2'
__author__ = 'Adrian Agnic'

class Block:

    def __init__(self, dictionary):
        self.__accepted_keys = ('data', 'index', 'nonce', 'prev_hash', 'destination', 'origin', 'timestamp')
        if isinstance(dictionary, dict): self.__set_properties(dictionary)

    def __repr__(self):
        return "Index: {},\n Hash: {},\n PreviousHash: {},\n Timestamp: {}\n".format(self._properties['index'], self._properties['hash'], self._properties['prev_hash'], self._properties['timestamp'])

    def __set_properties(self, dictionary):
        if self.verify_dict(dictionary) is False: return None
        self._properties = {key: value for key, value in dictionary.items()}
        self._properties['hash'] = self.sha(self._properties)
        self.__properties = (self._properties['data'], self._properties['index'], self._properties['nonce'], self._properties['prev_hash'], self._properties['destination'], self._properties['origin'], self._properties['timestamp'], self._properties['hash'])

    def get_accepted_keys(self):
        return self.__accepted_keys

    def get_properties(self):
        return self.__properties

    def verify_dict(self, dictionary):# NOTE REFACTOR
        pass

    @staticmethod
    def sha(properties):
        cat = "{1}{2}{3}{4}{5}{6}{7}".format(properties['data'], properties['index'], properties['nonce'], properties['prev_hash'], properties['destination'], properties['origin'], properties['timestamp'])
        hashed = hashlib.sha256(cat.encode()).hexdigest()
        return hashed
