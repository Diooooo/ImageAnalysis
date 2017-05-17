import numpy as np
import cv2

hidden = cv2.imread("../../outputdata/hw1/result.jpg")

hiddenLayer = cv2.split(hidden)[0]
print hidden.shape
hiddenName = hiddenLayer.copy()
m, n = hiddenLayer.shape
for i in range(m):
    for j in range(n):
        hiddenName[i, j] = hiddenLayer[i, j] % 2
        if hiddenName[i, j] == 0:
            hiddenName[i, j] = 255
        else:
            hiddenName[i, j] = 0

print hiddenName
# cv2.imwrite("../../outputdata/hw1/test.bmp", hiddenName)
# cv2.imshow("Name", hiddenName)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
