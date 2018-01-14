# ~ (WIP)

#### Developer:
Adrian Agnic

##### Current Usage Instructions:
* Requirements:
  * python3
* Run:
  * """ cd tilde/python/ """
  * """ python """
  * """
    from blockchain import Blockchain
    bc = Blockchain()
    bc.add_new_block('Hello World')
    last_block = bc.get_latest_block()
    last_block_info = last_block.get_properties()
    certain_info = bc.chain[3].get_properties()
    """
