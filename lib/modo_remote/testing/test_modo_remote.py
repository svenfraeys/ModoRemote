import os
import sys
# add library
library_folder_path = os.path.abspath(os.path.join(__file__, "..", "..", "..") )
print(library_folder_path)

if library_folder_path not in sys.path:
    sys.path.append(library_folder_path)

import modo_remote

def test_modo():
    modo_remote.run_python_script("/Users/Giu/Library/Application Support/Sublime Text 3/Packages/ModoRemote/examples/hello_modo.py", "localhost", 12357)

if __name__ == '__main__':  
    test_modo()