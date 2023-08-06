from PyQt5.QtWidgets import *

import src.__init__ as init

class aboutDialog(QDialog):
    """main class for the "about" dialooooooog that displays some information on the author etc.

    Args:
        QDialog (_type_): self
    """
    def __init__(self):
        super().__init__()

        # initialize layout and buttonbox
        self.layout = QVBoxLayout()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)

        # initialize the Textbox
        self.text_edit = QLabel(
            f"""
<head>
    <meta charset="utf-8" />
    <meta name="generator" content="pandoc" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
</head>
<body>
    <section id="menga-chart" class="level2">
        <h2>{init.name}</h2>
        <p><sub><em>{init.version}</em></sub></p>
        <p><strong>Application for editing indexed PNGs palettes. Mainly used for the creation of MES textures. </strong></p>
        <p>Contact us: </p>
        <ul>
            <li><a href="https://github.com/menga-tema/menga0chart">website</a>: https://github.com/menga-tema/menga</li>
            <li><a href="{init.email}">email</a>: {init.email}</li>
            <li>shouting (very hard)</li>
        </ul>
        <p>Copyright © 2022 menga-team;</p>
        <p><em>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
                associated documentation files (the “Software”), to deal in the Software without restriction, including
                without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
                following conditions:</em></p>
        <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions
            of the Software.</p>
        <p><strong>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
                LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
                NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
                WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
                SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</strong></p>
    </section>
</body>
</html>
        """
        )
        self.text_edit.setWordWrap(True)
        self.layout.addWidget(self.text_edit)

        self.button_box.accepted.connect(self.accept)

        self.setWindowTitle("About")
        self.setLayout(self.layout)


    @staticmethod
    def displayDialog():
        """conviniency function that declares a aboutDialog() and starts it
        """
        d = aboutDialog()
        d.exec()