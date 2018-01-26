import json
import copy
from flask import Flask, request

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

class Buffer:
    def __init__(self):
        self.list = []

    def size(self):
        return len(self.list)

bfr = Buffer()
app = Flask(__name__.split('.')[0])

def index():
    return '~'

# def send():
#     origin = request.args.get('origin', '')
#     dest = request.args.get('dest', '')
#     msg = request.args.get('msg', '')
#     print(origin, dest, msg)
#     bfr.list.append([origin, dest, msg])
#     return 'Success', 202
#
# def mine():
#     if (bfr.size() > 0):
#         queue_copy = copy.deepcopy(bfr.list)
#         bfr.list = []
#         return json.dumps(queue_copy), 200
#     else:
#         return 'No Messages', 400
#
#
# app.add_url_rule('/send', 'send', send, methods=['GET'])
# app.add_url_rule('/mine', 'mine', mine, methods=['GET'])

app.add_url_rule('/', 'index', index, methods=['GET'])

def start():
    app.run()
if __name__ == '__main__':
    start()
