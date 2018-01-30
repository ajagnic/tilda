import hashlib

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Block:

    __slots__ = ['index', 'hash', 'header', '__ps']

    def __init__(self, header_dict):
        for k,v in header_dict.items():
            self.__setattr__(k,v)
        self.set()

    def set(self):
        dct = {'index': self.index, 'hash': self.hash, 'header': self.header}
        self.__ps = list(dct.items())

    def pow(self, dictionary, difficulty):
        hashed = self.sha(dictionary)
        while hashed[:difficulty] != '0' * difficulty:
            dictionary['nonce'] += 1
            hashed = self.sha(dictionary)
        return dictionary

    def sha(self):
        cat = "{}".format(self.header)
        self.hash = hashlib.sha256(cat.encode()).hexdigest()

    @staticmethod
    def open_sha(plain):
        return hashlib.sha256(plain.encode()).hexdigest()

    @staticmethod
    def generate_header(previous_block):
        """
        generate header from given params tbd
        """
        new_header = {
            'index': 0,
            'version': __version__,
            'timestamp': 0,
            'previousHash': 0000000000000000000,
            'difficulty': 0,
            'nonce': 0,
            'body': 0
        }
        return new_header
