from flask import Flask

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

app = Flask(__name__.split('.')[0])

def index():
    return 'UP'

app.add_url_rule('/', 'index', index, methods=['GET'])

def start():
    app.run()
if __name__ == '__main__':
    start()
