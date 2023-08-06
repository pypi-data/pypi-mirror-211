from datetime import datetime

import cv2
import numpy as np


class AdditionalModel:
    def __init__(self):
        pass

    @classmethod
    def check_status(cls):
        print("Additional Model is Imported")

    @classmethod
    def read_image(cls, path_image):
        image = cv2.imread(path_image)
        if image is None:
            raise FileNotFoundError("`{}` cannot be loaded".format(path_image))
        return image

    @classmethod
    def rotate_image(cls, src, angle, center=None, scale=1.0):
        h, w = src.shape[:2]
        if center is None:
            center = (w / 2, h / 2)
        m = cv2.getRotationMatrix2D(center, angle, scale)
        try:
            rotated = cv2.warpAffine(src, m, (w, h))
        except:
            rotated = src
        return rotated

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

    def draw_text(self, image, text, coordinate, font=cv2.FONT_HERSHEY_SIMPLEX,
                  fontScale=None, color=(255, 0, 0), thickness=None):
        if fontScale is None:
            fontScale = self.__point_size(image)
        if thickness is None:
            thickness = self.__thickness(image)
        return cv2.putText(image, text, coordinate, font, fontScale, color, thickness, cv2.LINE_AA)

    def draw_circle(self, image, coordinate, radius=10, color=(255, 0, 0), fill=False, thickness=None):
        if thickness is None:
            thickness = self.__thickness(image)
        if fill:
            thickness = -1
        return cv2.circle(image, coordinate, radius, color, thickness)

    def draw_polylines(self, image, point, isClosed=True, color=(255, 0, 0), thickness=None):
        pts = np.array([point], np.int32)
        if thickness is None:
            thickness = self.__thickness(image)
        return cv2.polylines(image, [pts], isClosed, color, thickness)

    def draw_plus(self, image, coordinate, color=(255, 0, 0), size=None, thickness=2):
        x, y = coordinate
        if size is None:
            size = self.__point_size(image) * 2
        if thickness is None:
            thickness = int(self.__thickness(image))
        cv2.line(image, (x + size, y), (x - size, y), color, thickness)
        return cv2.line(image, (x, y + size), (x, y - size), color, thickness)

    def draw_line(self, image, coordinate_start, coordinate_end, color=(0, 0, 255), thickness=None):
        if thickness is None:
            thickness = self.__thickness(image)
        return cv2.line(image, coordinate_start, coordinate_end, color, thickness)

    def draw_cross(self, image, coordinate, color=(0, 0, 255), size=None, thickness=None):
        x, y = coordinate
        if size is None:
            size = self.__point_size(image)
        if thickness is None:
            thickness = self.__thickness(image)
        cv2.line(image, (x + size, y + size), (x - size, y - size), color, thickness)
        return cv2.line(image, (x + size, y - size), (x - size, y + size), color, thickness)

    def draw_square(self, image, coordinate, color=(255, 255, 255), size=None, thickness=None):
        x, y = coordinate
        if size is None:
            size = self.__point_size(image)
        if thickness is None:
            thickness = self.__thickness(image)
        return cv2.rectangle(image, (x + size, y + size), (x - size, y - size), color, thickness)

    def draw_triangle(self, image, coordinate, color=(255, 255, 255), size=None, thickness=None):
        x, y = coordinate
        if size is None:
            size = self.__point_size(image)
        if thickness is None:
            thickness = self.__thickness(image)

        cv2.line(image, (x, y - size), (x - size, y + size), color, thickness)
        cv2.line(image, (x, y - size), (x + size, y + size), color, thickness)
        return cv2.line(image, (x + size, y + size), (x - size, y + size), color, thickness)

    @classmethod
    def __point_size(cls, image):
        h, w = image.shape[:2]
        if w >= h:
            return h // 150
        if h > w:
            return w // 150

    @classmethod
    def __thickness(cls, image):
        h, w = image.shape[:2]
        if w >= h:
            return h // 350
        if h > w:
            return w // 350

    @classmethod
    def crop_small_image(cls, image, x, y, width_size):
        img = image[y - int(width_size / 2): (y - int(width_size / 2)) + width_size,
              x - int(width_size / 2):(x - int(width_size / 2)) + width_size]
        return img

    @classmethod
    def remap_image(cls, image, map_x, map_y):
        return cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)

    @staticmethod
    def save_image(image, dst_directory):
        ss = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
        name = dst_directory + "/" + str(ss) + ".png"
        cv2.imwrite(name, image)
        return name
