import json

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Tilde:

    __slots__ = ["bc"]

    def __init__(self, filename, difficulty):
        self.filecheck(str(filepath))
        self.bc = Blockchain(int(difficulty))

    def filecheck(self):
        try:
            with open(filepath, "r") as doc:
                chain_data = json.load(doc)
            doc.close()
            # init blockchain w/ chain_data
        except:
            self.bc.genesis()
            with open(filepath, "w") as doc:
                json.dump(self.bc.chain, doc, separators=(",", ":"))
            doc.close()
        else:
            # validate and return


class Blockchain:

    __slots__ = ["difficulty", "chain"]

    def __init__(self, difficulty):
        self.difficulty = int(difficulty)

    def genesis(self):# NOTE TODO BLOCK INIT COULD CHANGE
        self.chain = [Block(self.__proof_of_work({'data': 'Genesis', 'index': 0, 'nonce': 0, 'prev_hash': 0, 'destination': 0, 'origin': 0, 'timestamp': time.time()}))]


class Block:

    __slots__ = []

    def __init__(self, data):
        pass
