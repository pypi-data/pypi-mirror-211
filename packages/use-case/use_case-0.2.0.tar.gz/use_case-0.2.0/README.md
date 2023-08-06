Last update: 02/06/2023

# Steps:

1. Anaconda environment
2. Install poetry
   1. $conda install -c conda-forge poetry
3. Create project using poetry
   1. $poetry new use_case
4. Add the required libraries
   1. $poetry add LIBRARY
5. Test the library
   1. Install Pytest
      1. pip install pytest
   2. Run the tests: 
      1. $pytest -v .\tests\tests.py

### Publish library 
1. Build the project
   1. poetry build
2. Publish the project
   1. poetry publish
3. Install the created libraries (public access by default)
   1. $pip install use-case
   2. It will make only accessible the libraries


# Main features: 

* PEP 8 --> Style Guide
  * PyCharm native 
  * VSCode using Pylint (lastest python version supported 3.7) 

* PEP 257 –> Docstyle 
* Notebooks 
  * PyCharm visualization 
  * VSCode visualization and execution 
* Remote connection 
  * PyCharm ??? 
  * VSCode possible 
* Plugins 
  * LiveShare 
    * Git 
  * Docker 
  * Copilot (Kite)
* Testing 
  * PyCharm native 
  * VSCode ??? 
* Macros 
  * PyCharm possible
    * Eg, heading 
  * VSCode ??? 