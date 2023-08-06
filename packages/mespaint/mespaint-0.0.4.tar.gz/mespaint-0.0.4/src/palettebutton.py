from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class color_button(QToolButton):

    def __init__(self, color, index, palette):
        super().__init__()
        self.colorDialog = QColorDialog()
        self.colorDialog.setOption(QColorDialog.NoButtons)
        self.colorDialog.setOption(QColorDialog.ShowAlphaChannel)
        self.colorDialog.setOption(QColorDialog.DontUseNativeDialog)

        self.color = color
        self.index = index
        self.palette = palette

        self.clicked.connect(lambda: self.update_color(self.colorDialog.getColor(self.color)))
        self.update_color(color)

    def update_color(self, color):
        p = QPalette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        self.palette.colors[self.index] = color


class Palettebutton(QPushButton):
    def __init__(self, palette, parent):
        super().__init__()
        # self.setFlat(True)
        self.palette = palette
        self.parent = parent
        self.last_scroll = 0
        self.start_pos = QPoint()
        self.dragging = False
        self.last_y_mouse_pos = 0
        self.selected = False
        self.new_index = 0

        self.color_buttons = [
            color_button(self.palette.colors[0], 0, self.palette),
            color_button(self.palette.colors[1], 1, self.palette),
            color_button(self.palette.colors[2], 2, self.palette),
            color_button(self.palette.colors[3], 3, self.palette),
            color_button(self.palette.colors[4], 4, self.palette),
            color_button(self.palette.colors[5], 5, self.palette),
            color_button(self.palette.colors[6], 6, self.palette),
            color_button(self.palette.colors[7], 7, self.palette)
        ]
        self.name_edit = QLineEdit()
        self.remove_button = QToolButton()

        self.name_edit.setText(self.palette.name)
        self.name_edit.setPlaceholderText("insert Palette name")
        self.name_edit.textEdited.connect(self.change_name)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.remove_button.setIcon(self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.delete)

        self.layout.addWidget(self.name_edit, 0, 0, 1, 8)
        for i in range(8):
            self.layout.addWidget(self.color_buttons[i], 1, i)
        self.layout.addWidget(self.remove_button, 0, 8, 0, 1)

        self.setCheckable(True)
        self.setLayout(self.layout)
        self.setFixedWidth(370)
        self.setMinimumHeight(90)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.RightButton and self.hasMouseTracking():
            self.move(self.start_pos.x() + 30, self.start_pos.y() + (event.globalY() - self.last_y_mouse_pos) + (
                    self.parent.scroll.verticalScrollBar().value() - self.last_scroll))
            j = 0
            for i in self.parent.palette_buttons:
                if i.selected and i != self:
                    j += 1
                    i.chain_drag(event, self.x(), self.y(), offset=j)
            y = self.y() + event.y()
            for i in range(len(self.parent.palette_buttons) + 1):
                if y > 9 + ((i - 1) * 96) + 45:
                    self.parent.blue_line_widget.setGeometry(3, 9 + (i * 96) - 4, 400 + 6, 3)
                    self.new_index = i
                else:
                    break
                # for i in self.editor.palette_buttons
        else:
            self.parent.blue_line_widget.setGeometry(3, -5, 400 + 6, 3)

        super().mouseMoveEvent(event)

    def chain_drag(self, event, x, y, offset):
        self.move(x + (30 * offset), y + (30 * offset))

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.type() == QEvent.MouseButtonPress and e.button() == Qt.MiddleButton:
            self.setChecked(not self.isChecked())
            self.selected = not self.selected
            return
        if e.type() == QEvent.MouseButtonPress and e.button() == Qt.LeftButton:
            for i in self.parent.palette_buttons:
                i.setChecked(False)
            if self.parent.tabs.currentWidget() is not None and self.parent.tabs.currentWidget().isCanvas:
                # if i.selected:
                self.parent.tabs.currentWidget().set_palette(self.palette)
        if e.type() == QEvent.MouseButtonPress and e.button() == Qt.RightButton:
            self.setMouseTracking(True)
            self.dragging = True
            self.last_y_mouse_pos = e.globalY()
            self.last_scroll = self.parent.scroll.verticalScrollBar().value()
            self.start_pos = self.pos()
            self.mouseMoveEvent(e)
            # self.setHidden(True)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.type() == QEvent.MouseButtonRelease and e.button() == Qt.RightButton:
            self.setMouseTracking(False)
            self.dragging = False
            self.move(self.start_pos.x(), self.y())
            self.parent.blue_line_widget.setGeometry(3, -5, 400 + 6, 3)

            for i in reversed(range(self.parent.scroll_layout.count())):
                self.parent.scroll_layout.itemAt(i).widget().setParent(None)
            selected = []
            unselected = []
            for button in self.parent.palette_buttons:
                if button.selected or button == self:
                    selected.append(button)
                    unselected.append(None)
                else:
                    unselected.append(button)
            unselected = unselected[:self.new_index] + selected + unselected[self.new_index:]
            self.parent.palette_buttons = [button for button in unselected if button is not None]
            self.parent.palettes = [i.palette for i in self.parent.palette_buttons]
            for button in self.parent.palette_buttons:
                self.parent.scroll_layout.addWidget(button)
            return
        super().mouseReleaseEvent(e)

    def delete(self):
        for i in reversed(range(self.parent.scroll_layout.count())):
            self.parent.scroll_layout.itemAt(i).widget().setParent(None)
        self.parent.palette_buttons.remove(self)
        self.parent.palettes = [i.palette for i in self.parent.palette_buttons]
        for button in self.parent.palette_buttons:
            self.parent.scroll_layout.addWidget(button)

    def change_name(self):
        self.palette.name = self.name_edit.text()
