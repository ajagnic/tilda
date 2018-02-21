import unittest
from blockchain.master import Tilde

__author__ = "Adrian Agnic"
__version__ = "0.0.1"


class TestMaster(unittest.TestCase):
    def setUp(self):
        self.tilde = Tilde("test.db")
        print(tilde)

if __name__ == '__main__':
    unittest.main()
