from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import src.__init__ as init

class initTab(QWidget):
    def __init__(self, window):
        super().__init__()
        self.Title = QLabel(f"""
        <h2>{init.name}</h2>
        <p><sub><em>{init.version}</em></sub></p>
        <h3>Ha ha... MS-Paint, MES-Paint... get it? </h3>
        <br>
        """)
        self.window = window
        self.isCanvas = False
        self.openImage = QPushButton("Open Image")
        self.openImage.setStyleSheet('color: blue')
        self.openImage.setIcon(self.openImage.style().standardIcon(QStyle.SP_FileIcon))
        self.openImage.setFlat(True)
        self.openImage.clicked.connect(self.window.menubar.open_new_image)

        self.openPalette = QPushButton("Open Palette")
        self.openPalette.setStyleSheet('color: blue')
        self.openPalette.setIcon(self.openImage.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.openPalette.setFlat(True)
        self.openPalette.clicked.connect(self.window.menubar.open_palette_function)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.Title)
        self.layout.addWidget(self.openImage)
        self.layout.addWidget(self.openPalette)
        self.setLayout(self.layout)
