import sys

from PyQt5.QtWidgets import *

from src import utils, mainwindow

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


def main():
    utils.Exeption_handler(mainwindow.Mainwindow, app)


if __name__ == "__main__":
    main()
