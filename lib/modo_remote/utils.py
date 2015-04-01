"""utils for modo_remote
"""
import sys
sys.path.append("/Users/Giu/Library/Application Support/Sublime Text 3/Packages/ModoRemote/lib")

import modosock

def run_python_script(script_filepath, host, port):
    """run python script in given host and port
    """
    command = "script.run '%s'" % script_filepath
    print(command)
    command = '@"%s"' % script_filepath
    lx = modosock.ModoSock(host, port)
    lx.eval(command)
    lx.close()
    
def construct_modo_telnet_command(host, port):
    """return the modo command string that will open the port
    """
    modo_command = "telnet.listen %s true" % port
    return modo_command