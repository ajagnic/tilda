"""
Master module containing block, blockchain, and interface classes.
*   interface mimics sqlite3 usage
"""
import os

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Tilde:

    __slots__ = ["dbfile", "doc"]

    def __init__(self, filename, difficulty):
        self.dbfile = filename
        self.bc = Blockchain(difficulty)

    def connect(self):
        files = os.listdir()
        if ".chaindata" in  files:
            self.doc = ".chaindata/data"
            try:
                doc = open(self.doc, "r")
                doc.close()
            except:
                return False
            return True
        return False

    def save(self, data):
        """ add new block """
        pass

    def commit(self):
        """ mine """
        pass

    def find(self):
        """ query method, this will be hard """
        pass



class Blockchain:

    def __init__(self, difficulty):
        pass


class Block:

    def __init__(self):
        pass
