from flask import Flask, request

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

app = Flask(__name__.split('.')[0])


def index():
    return '~'

def inbox():
    msg = request.data
    print(msg)
    return msg, 200


app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/inbox', 'inbox', inbox, methods=['POST'])


def start():
    app.run()
if __name__ == '__main__':
    start()
