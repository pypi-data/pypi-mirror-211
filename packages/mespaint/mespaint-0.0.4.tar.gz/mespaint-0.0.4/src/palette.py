import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

from src import utils, palettebutton


class Palette:
    main = None

    def __init__(self, name, colors):
        self.colors = colors
        self.name = name
        self.button = None

    def change_name(self, name):
        self.name = name

    def change_color(self, color_index, color):
        self.colors[color_index] = color

    @staticmethod
    def open_from_file():
        filter = "Json files (*.json);;Text files (*.txt);;All files (*)"
        caption = "select json file to import"
        directory = os.path.expanduser('~')
        if path := QFileDialog.getOpenFileName(filter=filter, caption=caption, directory=directory)[0]:
            message = "There was an error reading the json file"

            def func():
                data = json.load(open(path))
                if "type" in data.keys() and "data" in data.keys():
                    if data["type"] == "palettes":
                        pl = [Palette.from_dict(j) for j in data["data"]]
                        for j in pl:
                            j.button = palettebutton.Palettebutton(j, Palette.main)
                            Palette.main.scroll_layout.addWidget(j.button)
                            Palette.main.palette_buttons.append(j.button)

            d = utils.Exeption_handler(func, silent=False, message=message)

    @staticmethod
    def save_palettes_to_file(palettes):
        filter = "Json files (*.json);;Text files (*.txt);;All files (*)"
        caption = "select a save location"
        directory = os.path.expanduser('~')
        overhead = {
            "type": "palettes",
            "data": [i.to_dict() for i in palettes]
        }
        if path := QFileDialog.getSaveFileName(filter=filter, caption=caption, directory=directory)[0]:
            message = "There was an error saving the json file"

            def func(): return json.dump(overhead, open(path, "w"), indent=2)

            utils.Exeption_handler(func, silent=True, message=message)

    def to_dict(self):
        return {
            "name": self.name,
            "colors": [i.rgb() for i in self.colors]
        }

    @staticmethod
    def from_dict(data):
        return Palette(data["name"], [QColor.fromRgb(i) for i in data["colors"]])