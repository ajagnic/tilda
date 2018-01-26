import click
import requests

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'

# NOTE pip install --editable .

@click.group()
def tilde():
    pass

@click.command()
@click.option('-m', type=str, prompt=True)
def send(m):
    ret = requests.post('http://localhost:5000/inbox', data=m)
    print(ret.text)

tilde.add_command(send)
