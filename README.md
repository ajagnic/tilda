# ~

###### Developer:
Adrian Agnic <https://github.com/ajagnic>

##### Description:
A Python blockchain data structure. Chain reverts to valid blocks on data manipulaton. 

###### Requirements:
* Python 3

##### Usage:

``` from blockchain import Blockchain ```

(assuming blockchain.py is in local folder)

``` bc = Blockchain() ```

(default difficulty value is 6, so this(and following blocks) may take a couple seconds to calculate)

``` bc.add_new_block(data, sender, recipient) ```

``` bc.save_local() ```

(saves blockchain data in JSON format in '.chaindata/')

###### Other:

To load a saved blockchain:

``` bc.load_local() ```

To change difficulty(or time to calculate):
* pass value on instantiation

``` bc = Blockchain(3) ```

Return latest block object in the chain:

``` bc.get_latest_block() ```
