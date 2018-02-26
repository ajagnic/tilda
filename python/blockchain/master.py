from time import time

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Tilde:

    def __init__(self):
        self.bc = Blockchain()

    def save(self, data):
        self.bc.add(data)



class Blockchain:

    def __init__(self):
        self.buffer = []

    def add(self, data):
        block = Block(data)
        self.buffer.append(block)



class Block:

    def __init__(self, data):
        self.__dict__.update(self.create(data))

    def create(self, data):
        block = {
            "body": {
                "meta": {
                    "timestamp": time()
                },
                "data": data
            }
        }
        return block
