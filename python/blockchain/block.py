import hashlib

__version__ = '0.0.2'
__author__ = 'Adrian Agnic'

class Block:
    """ Defines a block and its methods """

    def __init__(self, dictionary):
        """
        :param dictionary: only containing fields listed in get_accepted_keys()
        :type dictionary: dict
        """
        self.__accepted_keys = ('data', 'index', 'nonce', 'prev_hash', 'destination', 'origin', 'timestamp')
        if isinstance(dictionary, dict): self.__set_properties(dictionary)

    def __repr__(self):
        return "Index: {},\n Hash: {},\n PreviousHash: {},\n Timestamp: {}\n".format(self._properties['index'], self._properties['hash'], self._properties['prev_hash'], self._properties['timestamp'])

    def __set_properties(self, dictionary):
        if self.verify_dict(dictionary) is False: return None
        self._properties = {key: value for key, value in dictionary.items()}
        self._properties['hash'] = self.sha(self._properties)
        # store properties as immmutable
        self.__properties = (self._properties['data'], self._properties['index'], self._properties['nonce'], self._properties['prev_hash'], self._properties['destination'], self._properties['origin'], self._properties['timestamp'], self._properties['hash'])

    def get_accepted_keys(self):
        """ Return list of accepted keys to use for initializing a Block """
        return self.__accepted_keys

    def get_properties(self):
        """ Returns tuple of Block instance property values """
        return self.__properties

    def verify_dict(self, dictionary):
        if isinstance(dictionary, dict):
            if len(dictionary) == len(self.get_accepted_keys()):
                for key, value in dictionary.items():
                    if key in self.get_accepted_keys():
                        return True
        return False

    @staticmethod
    def sha(properties):# NOTE ADD VALIDATE TYPES
        """ Method that accepts fields of a Block, returns hash of all fields
        :param properties: properties of a Block instance
        :type properties: dict
        """
        cat = "{1}{2}{3}{4}{5}{6}{7}".format(properties['data'], properties['index'], properties['nonce'], properties['prev_hash'], properties['destination'], properties['origin'], properties['timestamp'])
        hashed = hashlib.sha256(cat.encode()).hexdigest()
        return hashed
