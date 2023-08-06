import os
import shutil

from PyQt6 import QtGui, QtCore, QtWidgets
import cv2


class AdditionalController:
    def __init__(self):
        pass

    @classmethod
    def check_status(cls):
        print("Additional Controller is Imported")

    @classmethod
    def select_directory(cls, parent=None, title='Select Folder'):
        option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(parent, title, options=option)
        return directory

    @classmethod
    def select_file(cls, parent, title, dir_path, file_filter):
        option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, title, dir_path, file_filter, options=option)
        return file_path

    @staticmethod
    def copy_directory(src_directory, dst_directory):
        directoryName = os.path.basename(src_directory)
        destinationPath = os.path.join(dst_directory, directoryName)
        shutil.copytree(src_directory, destinationPath)

    def show_image_to_label(self, label, image, width):
        height = self.calculate_height(image, width)
        image = self.resize_image(image, width)

        label.setMinimumSize(QtCore.QSize(width, height))
        label.setMaximumSize(QtCore.QSize(width, height))
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                             QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        label.setPixmap(QtGui.QPixmap.fromImage(image))

    @classmethod
    def calculate_height(cls, image, width):
        h, w = image.shape[:2]
        r = width / float(w)
        height = round(h * r)
        return height

    def get_cor_mouse_left_click_in_label_image(self, event, label, image):
        ratio_x, ratio_y = self.cal_ratio_image_label(label, image)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            pos_x = round(event.position().x() * ratio_x)
            pos_y = round(event.position().y() * ratio_y)
        else:
            pos_x, pos_y = None, None
        return pos_x, pos_y

    def get_cor_mouse_right_click_in_label_image(self, event, label, image):
        ratio_x, ratio_y = self.cal_ratio_image_label(label, image)
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            pos_x = round(event.position().x() * ratio_x)
            pos_y = round(event.position().y() * ratio_y)
        else:
            pos_x, pos_y = None, None
        return pos_x, pos_y

    def get_cor_mouse_move_event_in_label_image(self, event, label, image):
        pos_x = round(event.position().x())
        pos_y = round(event.position().y())
        ratio_x, ratio_y = self.cal_ratio_image_label(label, image)
        X = round(pos_x * ratio_x)
        Y = round(pos_y * ratio_y)
        return pos_x, pos_y, X, Y

    @classmethod
    def get_mouse_wheel(cls, event):
        angle = (event.angleDelta().y())
        return angle

    @classmethod
    def cal_ratio_image_label(cls, label, image):
        """
        Calculate the initial ratio of the image.

        Returns:
            ratio_x : ratio width between image and ui window.
            ratio_y : ratio height between image and ui window.
            center : find the center image on window user interface.
        """
        h = label.height()
        w = label.width()
        height, width = image.shape[:2]
        ratio_x = width / w
        ratio_y = height / h
        return ratio_x, ratio_y

    @classmethod
    def resize_image(cls, image, width):
        h, w = image.shape[:2]
        r = width / float(w)
        hi = round(h * r)
        try:
            result = cv2.resize(image, (width, hi),
                                interpolation=cv2.INTER_AREA)
        except:
            result = image
        return result
