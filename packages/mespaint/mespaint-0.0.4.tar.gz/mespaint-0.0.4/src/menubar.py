from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import webbrowser

from src import aboutdialog
from src import canvas
import src.__init__ as init
from src import palette


class MenuBar(QMenuBar):
    def __init__(self, window):
        super().__init__()
        self.window = window

        # >
        self.FileMenu = self.addMenu("File")
        # > File >
        self.OpenNewAction = self.FileMenu.addAction("Open new Image", self.open_new_image,
                                                     shortcut=QKeySequence("Ctrl+n"))
        self.ChangeAction = self.FileMenu.addAction("Change Image", self.change_image, shortcut=QKeySequence("Ctrl+o"))
        self.OpenPaletteAction = self.FileMenu.addAction("Open Palettes", self.open_palette_function,
                                                         shortcut=QKeySequence("Ctrl+Shift+o"))
        self.SaveMenu = self.FileMenu.addAction("Save Palettes", self.save_palette_function,
                                                shortcut=QKeySequence("Ctrl+Shift+s"))
        self.SaveImage = self.FileMenu.addAction("Save Image", self.save_image, shortcut=QKeySequence("Ctrl+s"))
        self.FileMenu.addSeparator()
        self.QuitAction = self.FileMenu.addAction("Quit", self.window.app.quit, shortcut=QKeySequence("Ctrl+q"))

        self.EditMenu = self.addMenu("Edit")
        self.selectAll = self.EditMenu.addAction("select all", self.window.select_all, shortcut=QKeySequence("Ctrl+a"))
        self.duplicate = self.EditMenu.addAction("duplicate palettes", self.window.duplicate_palettes,
                                                 shortcut=QKeySequence("Ctrl+d"))

        # >
        self.HelpMenu = self.addMenu("Help")
        # > Help >
        self.HelpAction = self.HelpMenu.addAction("Help", lambda: webbrowser.open(init.url),
                                                  shortcut=QKeySequence("Ctrl+h"))
        self.IssuesAction = self.HelpMenu.addAction("Issues/Report a Bug",
                                                    lambda: webbrowser.open(init.url + "/issues"),
                                                    shortcut=QKeySequence("Ctrl+Shift+h"))
        self.AboutAction = self.HelpMenu.addAction("About the application", aboutdialog.aboutDialog.displayDialog,
                                                   shortcut=QKeySequence("Ctrl+alt+h"))

    def change_image(self):
        canvs = canvas.Canvas(self.window)
        if canvs.open_from_file() is not None:
            index = self.parent().tabs.currentIndex()
            self.parent().tabs.removeTab(index)
            self.parent().tabs.insertTab(index, canvs, canvs.name)
            return True
        return False

    def open_new_image(self):
        canvs = canvas.Canvas(self.window)
        if canvs.open_from_file() is not None:
            self.parent().tabs.addTab(canvs, canvs.name)
            self.parent().tabs.setCurrentWidget(canvs)
            return True
        return False

    def save_image(self):
        if self.parent().tabs.currentWidget() is not None and self.parent().tabs.currentWidget().isCanvas:
            self.parent().tabs.currentWidget().save_to()

    def open_palette_function(self):
        palette.Palette.open_from_file()

    def save_palette_function(self):
        p = [i for i in self.window.palettes if i.button.isChecked()]
        palette.Palette.save_palettes_to_file(p)
