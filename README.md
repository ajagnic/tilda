# ~ (WIP)

#### Developer:
Adrian Agnic

### What is this
tilde will eventually be a local peer-to-peer networking client utilizing a blockchain structure for distributed storage

##### Current Usage Instructions:
* Requirements:
  * python3
##### Run:
  ```commandline
  cd tilde/python/
  ```
  Enter Python3 interpreter:
  ```commandline
  python
  ```
  ```commandline
  from blockchain.blockchain import Blockchain
  bc = Blockchain()
  bc.add_new_block('Hello World', 'me', 'you')
  bc.chain
  bc.save_local()
  bc.load_local()
  bc.validate_chain()
  ```

#### TODO:
* networking
* pretty big refactor w/ block structure
  * implement header/legitimate block struct
  * rely just on hash rather than immutables
  * double-sha 
* interface
* cythonize
* unittests
* Dockerfile
