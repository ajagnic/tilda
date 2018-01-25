import click
import requests
import json
from blockchain.blockchain import Blockchain

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

# NOTE pip install --editable .

@click.group()
def tilde():
    pass

@click.command()
@click.option('-o', type=str, prompt=True, help="Origin")
@click.option('-d', type=str, prompt=True, help="Destination")
@click.option('-m', prompt=True, help="Message")
def send(o, d, m):
    ret = requests.get('http://localhost:5000/send?origin={}&dest={}&msg={}'.format(o, d, m))
    print(ret.status_code, ret.text)

@click.command()
def mine():
    bc = Blockchain()
    bc.load_local()
    ret = requests.get('http://localhost:5000/mine')
    if ret.status_code == 200:
        ret_arr = json.loads(ret.text)
        for arr in ret_arr:
            bc.add_new_block(arr[2], arr[0], arr[1])
        print(bc.chain)
        bc.save_local()
    else:
        print(ret.text)



tilde.add_command(send)
tilde.add_command(mine)
