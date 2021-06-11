from PIL import Image

# import cv2 as cv
import numpy as np
import argparse, pytesseract, subprocess, time


class image_to_txt:
    """docstring for image_to_txt"""

    def __init__(self):
        pass

    def captcha_image_to_txt(self, img=None):
        if not img:
            img = "imagem.png"
        boundaries = [
            ([0, 0, 120], [120, 160, 255]),  # blue
            ([20, 80, 20], [160, 255, 150]),  # green
            ([200, 30, 30], [255, 90, 90]),  # red
            ([0, 0, 0], [50, 50, 50]),  # black
            ([90, 0, 150], [160, 50, 255]),  # purple
            ([220, 100, 0], [255, 180, 50]),  # orange
            ([130, 0, 90], [255, 100, 170]),  # pink
        ]
        img = cv.imread(img)
        cont = 0
        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            mask = cv.inRange(img, lower, upper)
            output = cv.bitwise_and(img, img, mask=mask)
            cv.imwrite("imagem_processada%s.png" % str(cont), output)
            text = (
                pytesseract.image_to_string(
                    Image.open("imagem_processada%s.png" % str(cont))
                )
                .replace(" ", "")
                .replace("\n", "")
            )
            cont += 1
            if text != "":
                return text
        return ""


if __name__ == "__main__":
    i = image_to_txt()
    print(i.captcha_image_to_txt())
