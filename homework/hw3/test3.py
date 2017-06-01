# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt
import cutborder


class Rectification:
    def __init__(self, img_path):
        self.img_path = img_path
        self.rotate_path = '../../outputdata/hw3/rotate.bmp'
        self.output_path = '../../outputdata/hw3/result.bmp'

    def rotate(self):
        """
        对初始图像进行矫正，并存储矫正结果
        :return: null
        """
        img = cv2.imread(self.img_path)                 # 读取图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 将RGB图像转换成灰度图
        gray = cv2.GaussianBlur(gray, (5, 5), 15)       # 对灰度图进行高斯模糊处理
        edged = cv2.Canny(gray, 240, 250)               # 使用Canny算法进行边缘检测

        lines = cv2.HoughLines(edged, 1, np.pi / 180, 118)  # 使用霍夫变换检测边界直线
        result = img.copy()
        result[...] = 0
        print len(lines[0])

        contours = []
        for i in range(len(lines[0])):
            '''
            求出边界直线交点作为待矫正图像顶点
            '''
            line1 = lines[0][i]
            r1 = line1[0]
            theta1 = line1[1]
            for j in range(i + 1, len(lines[0])):
                line2 = lines[0][j]
                r2 = line2[0]
                theta2 = line2[1]
                if theta2 == theta1:
                    continue
                else:
                    x0 = (r2 * np.sin(theta1) - r1 * np.sin(theta2)) / np.sin(theta1 - theta2)
                    y0 = r1 / np.sin(theta1) - (np.cos(theta1) / np.sin(theta1)) * x0
                    contours.append([y0, x0])
        print contours

        '''
        测试绘图
        '''
        # for line in lines[0]:
        #     rho = line[0]  # 第一个元素是距离rho
        #     theta = line[1]  # 第二个元素是角度theta
        #     print "rho", rho
        #     print "theta", theta
        #     if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):  # 垂直直线
        #         # 该直线与第一行的交点
        #         pt1 = (int(rho / np.cos(theta)), 0)
        #         # 该直线与最后一行的焦点
        #         pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])
        #         # 绘制一条白线
        #         cv2.line(result, pt1, pt2, 255)
        #     else:  # 水平直线
        #         # 该直线与第一列的交点
        #         pt1 = (0, int(rho / np.sin(theta)))
        #         # 该直线与最后一列的交点
        #         pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))
        #         # 绘制一条直线
        #         cv2.line(result, pt1, pt2, 255, 1)

        # for point in contours:
        #     print point
        #     cv2.circle(img, (point[1], point[0]), 5, (0, 0, 255), -1)
        #
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # exit()
        # contours.sort()

        '''
        对顶点进行排序以对应原图像顶点位置
        '''
        middle_x = sum(x[0] for x in contours) / len(contours)
        middle_y = sum(y[1] for y in contours) / len(contours)
        print middle_x, middle_y
        tmp = contours[:]
        print tmp
        for point in tmp:
            if point[0] < middle_x and point[1] < middle_y:
                contours[0] = point
            elif point[0] > middle_x and point[1] < middle_y:
                contours[1] = point
            elif point[0] > middle_x and point[1] > middle_y:
                contours[2] = point
            else:
                contours[3] = point

        src = np.float32(contours)
        des = np.float32([[0, 0], [img.shape[0], 0], [img.shape[0], img.shape[1]], [0, img.shape[1]]])

        M = cv2.getPerspectiveTransform(src, des)           # 生成透射矩阵

        rotate = cv2.warpPerspective(img, np.linalg.inv(M), (img.shape[1], img.shape[0]))    # 对原图像进行透射变换
        rotate = cutborder.rmBlackBorder(rotate, 20, 100, 2)
        cv2.imwrite(self.rotate_path, rotate)      # 去除图像黑边

    def markFlow(self):
        """
        标记图像内缺陷位置，并存储处理结果
        :return: null
        """
        origin = cv2.imread(self.img_path)
        rotate = cv2.imread(self.rotate_path)
        gray = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
        result = rotate.copy()
        m, n, _ = result.shape
        threshold = 60          # 阈值
        conn_threshold = 100    # 连通域阈值
        '''
            检测阈值并寻找连通域，染色为红
        '''
        for i in range(m):
            for j in range(n):
                if gray[i][j] < threshold:
                    result[i][j] = [255, 0, 0]
                    if i - 1 > 0 and gray[i - 1][j] < conn_threshold:
                        result[i - 1][j] = [255, 0, 0]
                        gray[i - 1][j] = threshold - 1
                    if i + 1 < m and gray[i + 1][j] < conn_threshold:
                        result[i + 1][j] = [255, 0, 0]
                        gray[i + 1][j] = threshold - 1
                    if j - 1 > 0 and gray[i][j - 1] < conn_threshold:
                        result[i][j - 1] = [255, 0, 0]
                        gray[i][j - 1] = threshold - 1
                    if j + 1 > n and gray[i][j + 1] < conn_threshold:
                        result[i][j + 1] = [255, 0, 0]
                        gray[i][j + 1] = threshold - 1
        cv2.imwrite(self.output_path, result)
        plt.subplot(211)
        plt.imshow(origin)
        plt.subplot(212)
        plt.imshow(result)
        plt.show()


if __name__ == '__main__':
    rectify = Rectification('../../testdata/hw3/hw3.bmp')
    rectify.rotate()
    rectify.markFlow()
