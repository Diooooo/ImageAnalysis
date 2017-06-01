# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


class MsgHide:
    def __init__(self, image_path, hidden_msg):
        self.image_path = image_path
        self.hidden_msg = hidden_msg
        self.save_path = '../../outputdata/hw1/result.bmp'

    def hide(self):
        """
        将要隐藏信息的图片的red层的像素值偶数化，之后读取对应位置上需隐藏图片的像素值，若判定为黑色，则在
        原图片对应位置red层像素+1
        :return: 保存处理后的图片
        """
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
        """
        创建一个zeros矩阵，大小与处理过后的图片一致
        读取处理过后的图片red层的最后一位数值，输出到zeros矩阵中，若不为0则对应位置赋值白色像素值
        :return: 使用matplotlib.pyplot进行结果展示
        """
        origin = cv2.imread(self.image_path)
        img = cv2.imread(self.save_path)
        out = np.zeros(img.shape, img.dtype)
        width, height = img.shape[:2]
        for i in range(width):
            for j in range(height):
                if img[i, j, 2] % 2 == 0:
                    out[i, j, 0] = 255
                    out[i, j, 1] = 255
                    out[i, j, 2] = 255
        plt.subplot(221)
        plt.imshow(origin)
        plt.title('origin')
        plt.subplot(222)
        plt.imshow(img)
        plt.title('with hidden message')
        plt.subplot(223)
        plt.imshow(out)
        plt.title('hidden message')
        plt.show()


if __name__ == '__main__':
    demo = MsgHide('../../testdata/hw1/origin.bmp', '../../testdata/hw1/msg.bmp')
    demo.hide()
    demo.decipher()
