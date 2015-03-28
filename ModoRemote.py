"""modo remote functionality for sublime

telnet.listen 4000 true
"""
import sys
import os

# add library
library_folder_path = os.path.abspath(os.path.join(__file__, "..", "lib") )

if library_folder_path not in sys.path:
    sys.path.append(library_folder_path)

import modosock
import sublime
import sublime_plugin
import modo_remote
import traceback

HOST = "localhost"
PORT = 12357

# show python crashes
def display_exceptions_ui(func):
    """decorator function to show crashes as
    QtGui Messagebox to be certain artists see a problem
    
    Args:
        func (function): the function to be function
    Returns:
        function: wrapped function
    """
    def decorated_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except :
            error = 'Oops...something went wrong\n\n{error}'
            format_exc = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()

            error = error.format(error=format_exc)

            print("ERROR")
            print("-----")
            print(error)

            sublime.message_dialog(error)
    return decorated_function

class ModoRemoteOpenTelnetCommandToClipboard(sublime_plugin.WindowCommand):
    """place the command for modo in the clipboard
    """
    @display_exceptions_ui
    def run(self):
        """run the command
        """
        modo_command = modo_remote.construct_modo_telnet_command(HOST, PORT)
        sublime.set_clipboard(modo_command)

class ModoRemoteRunActiveScript(sublime_plugin.WindowCommand):
    """launch your active view in modo
    """
    @display_exceptions_ui
    def run(self):
        """run the script
        """
        window = sublime.active_window()

        if not window:
            sublime.message_dialog("no active window")
            return

        view = window.active_view()

        if not view:
            sublime.message_dialog("no active window")
            return

        file_name = view.file_name()

        if not file_name:
            sublime.message_dialog("please save your current file")
            return

        # run script in modo
        print("running script %s (%s %s)" % (file_name, HOST, PORT) )
        modo_remote.run_python_script(file_name, HOST, PORT)



# lx = modosock.ModoSock("localhost", 80)
# lx.eval("s")
# modo_remote.run_python_script("/Users/Giu/Library/Application Support/Sublime Text 3/Packages/ModoRemote/examples/hello_modo.py", "localhost", 12357)

