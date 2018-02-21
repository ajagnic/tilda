"""
Master module containing block, blockchain, and interface classes.
*   interface mimics sqlite3 usage
"""

__author__ = "Adrian Agnic"
__version__ = "0.0.1"


class Tilde:

    def __init__(self, filename):
        self.filename = filename
        self.connect()

    def connect(self):
        """ check local directory, create db file """
        pass
