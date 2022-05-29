import cv2
import numpy as np
import time
from math import sqrt

# ЗНАЧЕНИЯ ПЕРЕМЕННЫХ ВНУТРИ ФУНКЦИИ
# (ОНА БУДЕТ МЕТОДОМ КЛАССА С РАСПОЗНАВАНИЕМ МАРШРУТА И РАЗЛИВОВ)

# координаты повреждения
RUPTURE_CX = 0
RUPTURE_CY = 0

# время, прошедшее с начала детектирования разлива
OIL_TIME = 0

# флаг, указывающий наличие разлива
OIL = False

# площадь разлива в пикселях
OIL_AREA = 0.0

# время, которое должно пройти с нахождения разлива для его учета
OIL_THR = 0.1

# толщина линии
LINE_WIDTH = 3

# цвет области с найденным разливом
OIL_COLOR = (255, 0, 0)


def detect_oil(self, image, draw, oil_time, oil, oil_thr, oil_color, line_width, rupture_cx, rupture_cy):
    # для рисования
    draw = draw.copy()
    oil_image = image.copy()
    height, width = image.shape

    # бинаризуем из цветового пространства HSV по пороговым значениям
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    bin_line = cv2.inRange(hsv, (23, 48, 141), (52, 255, 255))
    bin_colors = cv2.inRange(hsv, (0, 48, 141), (52, 255, 255))
    bin = cv2.bitwise_xor(bin_colors, bin_line)
    kernel = np.ones((5, 5), np.uint8)
    bin = cv2.erode(bin, kernel)

    # вырезаем участок изображения, на котором введем поиск разлива
    y_st = max(0, rupture_cy - 90)
    y_ed = min(height, rupture_cy + 90)
    bin = bin[y_st:y_ed, :]
    kernel = np.ones((3, 3), np.uint8)
    bin = cv2.erode(bin, kernel)
    bin = cv2.dilate(bin, kernel)

    # поиск контуров разливов
    contours = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    obj = [float('inf'), 0, 0]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if cv2.contourArea(cnt) > 750:
            x, y, w, h = cv2.boundingRect(cnt)
            dst = sqrt((rupture_cx - x) ** 2 + (rupture_cy - y) ** 2)
            if obj[0] > dst:
                obj = [dst, cnt, area]

    if obj[0] != float('inf'):
        now = time.time()
        if oil_time == 0 and (not oil):
            oil_time = now
        elif oil_time > 0 and (not oil) and (now - oil_time) >= oil_thr:
            oil = True
            oil_area = obj[2]
            oil_time = 0

        oil_image[rupture_cy - 90:rupture_cy + 90, :] = \
            cv2.drawContours(oil_image[rupture_cy - 90:rupture_cy + 90, :], \
                             [obj[1]], 0, oil_color, line_width)
        draw[rupture_cy - 90:self.rupture_cy + 90, :] = \
            cv2.drawContours(draw[rupture_cy - 90:rupture_cy + 90, :], \
                             [obj[1]], 0, oil_color, line_width)
    else:
        oil_time = 0

    return draw, oil_image
