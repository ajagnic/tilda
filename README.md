# ~ (WIP)

#### Developer:
Adrian Agnic

##### Current Usage Instructions:
* Requirements:
  * python3
* Run:
  * ```commandline
    cd tilde/python/
    ```
  * Enter Python3 interpreter:
    * ```commandline
      python
      ```
  * ```commandline
    from blockchain import Blockchain
    bc = Blockchain()
    bc.add_new_block('Hello World', 'me', 'you')
    bc.chain
    ```
##### Known Bugs:
* Mutable 'hash' value can be changed and passes validation
