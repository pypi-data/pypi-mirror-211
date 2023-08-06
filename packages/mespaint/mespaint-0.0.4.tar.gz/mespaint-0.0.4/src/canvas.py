from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os

from src import utils


class Canvas(QLabel):

    def __init__(self, window):
        super().__init__()
        self.isCanvas = True
        self.path = None
        self.image = QImage()
        self.name = "default"
        self.selected = False
        self.resize(self.width() - 10, self.height() - 10)
        # self.scroll_widget.wheelEvent = self.wheelEvent
        self.dragging = False
        self.last_mouse_pos = QPoint(0, 0)
        self.zoom = 1
        self.window = window
        self.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        # self.scroll_widget.resize(self, 1000)
        # self.setPixmap(QPixmap(self.image).scaledToWidth(int(self.width())))


    # def wheelEvent(self, event: QWheelEvent):
    #     self.scroll_widget.resize(self.width() - 10, self.height() - 5)
    #     if event.modifiers() == Qt.ControlModifier and event.angleDelta().x() == 0:
    #         print(event.angleDelta().y() / 1000, self.zoom)
    #         if event.angleDelta().y() > 0 and self.zoom < 3:
    #             self.zoom *= 1.05
    #             self.scroll_widget.setPixmap(
    #                 QPixmap(self.image).scaled(
    #                     int(self.scroll_widget.pixmap().width() * 1.05),
    #                     int(self.scroll_widget.pixmap().height() * 1.05),
    #                     Qt.KeepAspectRatio))
    #         elif event.angleDelta().y() < 0 and self.zoom > 0.3:
    #             self.zoom *= 0.95
    #             self.scroll_widget.setPixmap(
    #                 QPixmap(self.image).scaled(
    #                     int(self.scroll_widget.pixmap().width() * 0.95),
    #                     int(self.scroll_widget.pixmap().height() * 0.95),
    #                     Qt.KeepAspectRatio))

    def mousePressEvent(self, event: QMouseEvent):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.globalPos()
            self.last_widget_pos = self.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.dragging = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.type() == QEvent.MouseMove and self.dragging:
            self.move(self.last_widget_pos.x() + (event.globalPos().x() - self.last_mouse_pos.x()),
                      self.last_widget_pos.y() + (event.globalPos().y() - self.last_mouse_pos.y()))
        super().mouseMoveEvent(event)

    # def resizeEvent(self, event):
    #     # self.resize(self.width(), self.height())
    #     self.setPixmap(self.pixmap().scaled(self.width(), self.height(), Qt.KeepAspectRatio))
    #     super().resizeEvent(event)

    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    def open_from_file(self):
        filter = "Images (*.jpeg *.jpg *.png *.gif *.bmp);;All files (*)"
        caption = "select image file to import"
        directory = os.path.expanduser('~')
        if path := QFileDialog.getOpenFileName(filter=filter, caption=caption, directory=directory)[0]:
            message = "There was an error reading the image file"
            if utils.Exeption_handler(self.validate_path, path, message=message, silent=True):
                self.image.load(path)
                self.name = os.path.basename(path)
                if self.image.format() == QImage.Format_Indexed8:
                    if self.image.colorCount() > 8:
                        self.window.add_palette(self.name, [QColor(i) for i in self.image.colorTable()[:8]])
                    else:
                        self.window.add_palette(self.name, [QColor(i) for i in self.image.colorTable()])

                self.reload_preview()
                return path

    def save_to(self):
        filter = "Images (*.jpeg *.jpg *.png *.gif *.bmp);;All files (*)"
        caption = "select save location"
        directory = os.path.expanduser('~')
        if path := QFileDialog.getSaveFileName(filter=filter, caption=caption, directory=directory)[0]:
            message = "There was an error saving the image file"
            if utils.Exeption_handler(self.image.save, path, "PNG", message=message, silent=True):
                return path

    def validate_path(self, path):
        image = QImage(path)
        return path

    def reload_preview(self):
        # self.scroll_widget.pixmap().fill(Qt.black) self.scroll_widget.pixmap().conectr(self.image).scaled(int(
        # self.width() * 0.9), int(self.height() * 0.9), Qt.KeepAspectRatio)
        # self.scroll_widget.setPixmap(QPixmap(self.image).scaledToWidth(int(self.width())))
        # self.pixmap.fill(Qt.black)
        # self.setPixmap(self.pixmap)
        # self.scroll_widget.pixmap().
        # self.repaint()
        # self = Canvas(self.path)
        if not self.isCanvas:
            return
        pixmap = QPixmap()
        pixmap.convertFromImage(self.image)

        try:
            rectangle_aspect_ratio = pixmap.width() / pixmap.height()
            target_aspect_ratio = self.width() / self.height()
        except ZeroDivisionError:
            return

        # Determine the scaling factor for width and height
        if rectangle_aspect_ratio > target_aspect_ratio:
            scale_factor = self.width() / pixmap.width()
        else:
            scale_factor = self.height() / pixmap.height()

        # Calculate the new dimensions of the resized rectangle
        new_width = int(pixmap.width() * scale_factor * 0.9)
        new_height = int(pixmap.height() * scale_factor * 0.9)

        self.setPixmap(pixmap.scaled(new_width, new_height))

    def resizeEvent(self, *__args):
        super().resizeEvent(*__args)
        self.reload_preview()

    def set_palette(self, palette):
        # self.image.load(self.path)
        # self.image.setColorCount(8)
        # for i in range(8):
        #     self.image.setColor(i, palette.colors[i].rgb())
        # self.image.setColorTable([4278190080, 4278190080, 4278190080, 4278190080])
        if self.image.format() == QImage.Format_Indexed8:
            self.image.setColorTable([i.rgb() for i in palette.colors])
        else:
            self.image = self.image.convertToFormat(QImage.Format_Indexed8, [i.rgb() for i in palette.colors])
        # self.scroll_widget.
        # self.image = self.image.convertToFormat(QImage.Format_Indexed8)
        # self.image.fill(QColor(4278190080))
