import json
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.palette import Palette
from src import canvas, inittab
from src import palette, menubar, palettebutton


class Mainwindow(QMainWindow):
    def __init__(self, app):
        """Its the main window and parent of all Widgets and Dialog in the application.

        Args:
            app (QApp): needed to styart the programm
        """
        super().__init__()
        self.palettes = []
        Palette.main = self
        self.app = app
        self.show()
        self.setWindowTitle('MESpaint')
        self.menubar = menubar.MenuBar(self)
        self.setMenuBar(self.menubar)

        # initilize tabs and ui
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setTabBarAutoHide(False)
        # self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabCloseRequested.connect(self.tab_close)
        self.tabs.addTab(inittab.initTab(self), "Welcome")

        self.palette_buttons = []

        self.scroll = QScrollArea()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget = QWidget()
        self.blue_line_widget = QWidget(self.scroll_widget)
        self.scroll_master_layout = QVBoxLayout()
        self.add_subject_button = QPushButton()

        self.add_subject_button.setIcon(
            self.add_subject_button.style().standardIcon(QStyle.SP_ToolBarVerticalExtensionButton))
        self.add_subject_button.clicked.connect(lambda: self.add_palette())

        self.scroll_master_layout.addLayout(self.scroll_layout)
        self.scroll_master_layout.addWidget(self.add_subject_button)

        self.scroll_widget.setLayout(self.scroll_master_layout)

        self.scroll.setFixedWidth(400)
        self.scroll.setWidget(self.scroll_widget)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll.setPol
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        for i in self.palettes:
            i.button = palettebutton.Palettebutton(i, self)
            self.scroll_layout.addWidget(i.button)
            self.palette_buttons.append(i.button)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.tabs)
        temp = QWidget()
        temp.setLayout(self.layout)

        self.blue_line_widget.setAutoFillBackground(True)
        self.blue_line_widget.setStyleSheet("background-color:cyan;")
        self.blue_line_widget.setGeometry(3, -5, 400 + 6, 3)

        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_master_layout.setAlignment(Qt.AlignTop)

        self.setCentralWidget(temp)

        self.setAcceptDrops(True)

        # set the central widget, menubar and finally starts the eventloop of the application by calling exec()
        # self.setMenuBar(self.menubar)
        app.exec()

    def tab_close(self, index):
        self.tabs.removeTab(index)

    def select_all(self):
        for i in self.palettes:
            i.button.setChecked(True)
            i.button.selected = True

    def duplicate_palettes(self):
        for i in self.palettes:
            if i.button.selected:
                self.add_palette(i.name + "_", i.colors)

    def add_palette(self, name="new Palette", colors=None):
        if colors is None:
            colors = [QColor(), QColor(), QColor(), QColor(), QColor(), QColor(), QColor(), QColor()]
        palett = palette.Palette(name, colors)
        palett.button = palettebutton.Palettebutton(palett, self)
        self.palettes.append(palett)
        self.scroll_layout.addWidget(palett.button)
        self.palette_buttons.append(palett.button)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            try:
                img = QImage()
                if img.load(f):
                    canvs = canvas.Canvas(self)
                    canvs.name = os.path.basename(f)
                    canvs.image = img
                    if canvs.image.format() == QImage.Format_Indexed8:
                        if img.colorCount() > 8:
                            self.add_palette(canvs.name, [QColor(i) for i in canvs.image.colorTable()[:8]])
                        else:
                            self.add_palette(canvs.name, [QColor(i) for i in canvs.image.colorTable()])
                    index = self.tabs.currentIndex()
                    self.tabs.addTab(canvs, canvs.name)
                    self.tabs.setCurrentWidget(canvs)
                    canvs.reload_preview()
            except Exception as e:
                print(f"failed toload {f} as image", e)
            try:
                data = json.load(open(f))
                if "type" in data.keys() and "data" in data.keys():
                    if data["type"] == "palettes":
                        pl = [Palette.from_dict(j) for j in data["data"]]
                        for j in pl:
                            j.button = palettebutton.Palettebutton(j, Palette.main)
                            self.scroll_layout.addWidget(j.button)
                            self.palette_buttons.append(j.button)
            except Exception as e:
                print(f"failed toload {f} as json", e)
