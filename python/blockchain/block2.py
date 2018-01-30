import hashlib

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Block:

    __slots__ = ['index', 'hash', 'header', '__ps']

    def __init__(self, dictionary):
        for k,v in dictionary.items():
            self.__setattr__(k,v)
        self.set()

    def __repr__(self):
        return "Index: {0.index}, \n Hash: {0.hash}, \n Header: {0.header}\n".format(self)

    def set(self):
        dct = {'index': self.index, 'hash': self.hash, 'header': self.header}
        self.__ps = list(dct.items())

    def generate_header(self):
        """
        generate header from given params tbd
        """
        new_header = {
            'index': 0,
            'version': __version__,
            'timestamp': 0,
            'previousHash': 0000000000000000000,
            'difficulty': 0,
            'nonce': 0
        }
        return new_header


    # def pow(self, dictionary, difficulty):
    #     """
    #     Increment a property 'nonce' until the resulting hash has a leading amount of zeros equal to difficulty
    #     """
    #     hashed = self.sha(dictionary)
    #     while hashed[:difficulty] != '0' * difficulty:
    #         dictionary['nonce'] += 1
    #         hashed = self.sha(dictionary)
    #     return dictionary
    #
    # @staticmethod
    # def sha(properties):
    #     cat = "".format(!)
    #     hashed = hashlib.sha256(cat.encode()).hexdigest()
    #     return hashed
