# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


class MsgHide:
    def __init__(self, image_path, hidden_msg):
        self.image_path = image_path
        self.hidden_msg = hidden_msg
        self.save_path = '../../output.data/hw1/result.bmp'

    def hide(self):
        img = cv2.imread(self.image_path)
        msg = cv2.imread(self.hidden_msg)
        width, height = img.shape[:2]

        for i in range(width):
            for j in range(height):
                if img[i, j, 2] % 2 != 0:
                    img[i, j, 2] -= 1
                if msg[i, j, 0] == 0 and msg[i, j, 1] == 0 and msg[i, j, 2] == 0:
                    img[i, j, 2] += 1

        cv2.imwrite(self.save_path, img)

    def decipher(self):
        img = cv2.imread(self.save_path)
        out = np.zeros(img.shape, img.dtype)
        width, height = img.shape[:2]
        for i in range(width):
            for j in range(height):
                if img[i, j, 2] % 2 != 0:
                    out[i, j, 0] = 255
                    out[i, j, 1] = 255
                    out[i, j, 2] = 255
        plt.subplot(211)
        plt.imshow(img)
        plt.subplot(212)
        plt.imshow(out)
        plt.show()


if __name__ == '__main__':
    demo = MsgHide('../../testdata/hw1/origin.bmp', '../../testdata/hw1/msg.bmp')
    demo.hide()
    demo.decipher()
