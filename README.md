# ~ (WIP)

#### Developer:
Adrian Agnic

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
* pretty big refactor w/ block structure
  * rely just on hash rather than immutables
  * double-sha because thats better?
* cythonize
* unittests
* Dockerfile
