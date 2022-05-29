from pyzbar.pyzbar import decode
import cv2


def qr_code(self, image):
    boxes = decode(image)
    if len(boxes) == 0:
        return image
    for box in boxes:
        data = box.data.decode("utf-8").split('\n')
        if len(data) != 2:
            print('Error data format in Qr-code, skipping!')
            return image

        image = cv2.rectangle(image, (box.rect.left, box.rect.top), \
                              (box.rect.width + box.rect.left, box.rect.height + box.rect.top), \
                              self.qr_color, self.line_width)
        self.nav_area = data[0].split(' ')
        self.lake_area = data[1].split(' ')
        self.QR_detect = False
        break
    return image