from time import time
from hashlib import sha256

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Tilde:

    def __init__(self, hardness):
        self.bc = Blockchain(hardness)

    def save(self, data):
        self.bc.add(data)

    def commit(self):
        self.bc.mine()



class Blockchain:

    def __init__(self, hardness):
        self.x = hardness
        self.genesis()
        self.buffer = []

    def add(self, data):
        self.buffer.append(Block(data))

    def mine(self):
        for block in self.buffer:
            latest = self.latest()
            block["body"]["meta"]["index"] = (latest["head"]["index"] + 1)
            block["body"]["meta"]["previous"] = latest["head"]["hash"]
            block = self.work(block)
            block.head()
            self.chain[str(block["head"]["index"])] = block

    def work(self, block):
        hashed = block.sha()
        while hashed[:self.x] != "0" * self.x:
            block["body"]["meta"]["nonce"] += 1
            hashed = block.sha()
        block["body"]["meta"]["hash"] = hashed
        return block

    def genesis(self):
        genesis = self.work(Block("genesis"))
        genesis.head()
        self.chain["0"] = genesis

    def latest(self):
        return self.chain[str(len(self.chain)-1)]



class Block:

    def __init__(self, data):
        self.__dict__.update(self.create(data))

    def create(self, data):
        block = {
            "body": {
                "meta": {
                    "timestamp": time(),
                    "nonce": 0
                },
                "data": data
            }
        }
        return block

    def sha(self):
        return sha256(sha256(self.__dict__.values.encode())).hexdigest()

    def head(self):
        hashed = self.sha()
        if self.__dict__["body"]["meta"]["hash"] == hashed:
            self.__dict__["head"] = {
                "index": self.__dict__["body"]["meta"]["index"],
                "hash": hashed
            }
