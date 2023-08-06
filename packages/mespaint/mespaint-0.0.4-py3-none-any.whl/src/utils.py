from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def Exeption_handler(func, *args, silent=False, message=None, **kwargs):
    """this method is just a way to execute a function in the most overprtected way possible
    it wraps in in a try catch and displays a ErrorDialog in case an error occurs

    Args:
        func (func): fucntion to execute
        silent (bool, optional): if True errors will not be raised, just the dialog be shown. Defaults to False.
        message (str, optional): errormessage to show in case the execution fails. Defaults to None.

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """
    try:
        return True, func(*args, **kwargs)
    except Exception as e:
        if message is not None:
            message = f"{str(e)}\n\n[{message}]"
        else:
            message = str(e)
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec()
        if not silent:
            raise e
        return False, message