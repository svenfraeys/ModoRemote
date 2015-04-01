# python
"""modo sock
adapatation applied from sven fraeys
This for support in python 3.0 in str to bytes convertion
"""
################################################################################
#
# modosock.py
#
# Version: 1.002
#
# Author: Gwynne Reddick
#
# Description: Wrapper for modo socket connection. uses modo's raw mode
# 
#
# Usage: Instantiate ModoSock class with hostname and port number. Use one of
#        the three eval commands to send command strings to modo. The eval
#        commands operate like their lx.eval counterparts
#
# Last Update 19:02 06/06/10 
#
################################################################################

import socket

# defines the end of a transmit from modo, it's actually the prompt character
# sent after the last result
_END = '> \0'  

# status codes
_ERROR = -1
_OK = 1
_INFO = 2


class ModoSockError(Exception):
    pass


class ModoError(ModoSockError):
    """Raised when an error message is received from modo
    
    Attributes:
        message  -  the error message sent from modo
        command  - the command that was executed
        
    """
    def __init__(self, command, value):
        self.value = value
        self.command = command
    def __str__(self):
        return '%s\ncommand string: %s' % (self.value, self.command)
    
    def get_error(self):
        return '%s\ncommand string: %s' % (self.value, self.command)


class UnrecognisedLineError(ModoSockError):
    """Raised when an incoming line is found that doesn't start with one of the
    known line start characters. This probably means that the current line is a
    continuation of the previous one.
    
    Attributes:
        command   -  command that was sent to modo
        prevline  -  text of line that was received before the error line
        currline  -  text of line that threw the error
    
    """
    
    def __init__(self, command, prevline, currline):
        self.command = command
        self.prevline = prevline
        self.currline = currline
        
    def __str__(self):
        return 'command: %s\nresult: %s\n%s' % (self.command, self.prevline, self.currline)
    
    def get_error(self):
        return 'command: %s\nresult: %s\n%s' % (self.command, self.prevline, self.currline)


class ModoSock(object):
    """Raw socket communication class.
    
    Wraps a socket connection for cummunicating with modo in raw mode. Implements
    three methods that work/behave like their lx module counterparts.
    
    """
    
    def __init__(self, host, port):
        try:
            self._con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._con.connect((host, port))
        except:
            raise
        self.status = _OK
        self.message = ''
        self._con.recv(1024)  # eat the first prompt character
    
    def close(self):
        """Close the connection with modo.
        
        Be sure to call this at the end of any script
        
        """
        
        self._con.close()
        
    def eval(self, command):
        """Send a command to modo.
        
        Unlike the regular lx.eval command in modo, this implementation does not
        return a value. It should therefore be used for executing in 'command'
        mode, ie for executing commands in modo that do not return a value - so don't
        use for queries!!!
        
        """
        
        result = self._get_result(command)
    
    def eval1(self, command):
        """Send a command to modo. Behaves like lx.eval1
        
        Return value is always either a singleton or None. If modo returns more
        than one result only the first will be returned by this function
        
        """
        
        result = self._get_result(command)
        if self.status == _OK:
            return result[0]
    
    def evalN(self, command):
        """Send a command to modo. Behaves like lx.evalN
        
        Return value is always either a list or None.
        
        """
        
        result = self._get_result(command)
        if self.status == _OK:
            return result
    
    def _get_result(self, command):
        result = []
        # send command
        send_command = bytes('%s\0' % command, 'UTF-8')
        self._con.sendall(send_command)
        alldata = ''
        # collect data
        while 1:
            data = self._con.recv(1024)
            data = data.decode('UTF-8')
            if not data: break
            if _END in data:
                alldata += data[:data.find(_END)]
                break
            alldata += data
        # process data
        alldata = alldata.split('\0')
        alldata.remove('')  # remove trailing blank line from alldata
        for item in alldata:
            if item.startswith('- error'):
                # modo has returned an error, set self.status to error and
                # self.message to the result value so they can be retrieved by
                # by calling scripts and then raise an error
                self.status = _ERROR
                self.message = item[2:]
                raise ModoError(command, item[2:])
            elif item[0] in ['#','!','@']:
                self.status = _INFO
                self.message = item
                break
            elif item.startswith('+ ok'):
                self.status = _OK
            elif item.startswith(':'):
                result.append(item[2:])
            else:
                raise UnrecognisedLineError(command, alldata[alldata.index(item)-1], item)
        return result