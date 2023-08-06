import cv2
import numpy as np
import qrcode
import pyzbar.pyzbar as pyzbar


class QRCode:

    def __init__(self):
        pass

    def generate(self, data: str):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    def detect(self, image: np.ndarray):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        codes = pyzbar.decode(gray)
        results = []
        for code in codes:
            result = {
                'data': code.data.decode('utf-8'),
                'type': code.type,
                'position': code.rect
            }
            results.append(result)
        return results

if __name__ == '__main__':
    qr = QRCode()
    img = qr.generate('hello world')
    img.save('hello_world.png')
