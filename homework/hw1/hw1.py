import cv2
import numpy as np

pigeon = cv2.imread("../../testdata/hw1/pigeon.jpg")
name = cv2.imread("../../testdata/hw1/name.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)

# blue = np.zeros((pigeon.shape[0], pigeon.shape[1]), dtype=pigeon.dtype)
# green = np.zeros((pigeon.shape[0], pigeon.shape[1]), dtype=pigeon.dtype)
# red = np.zeros((pigeon.shape[0], pigeon.shape[1]), dtype=pigeon.dtype)
#
# blue[:, :] = pigeon[:, :, 0]
# green[:, :] = pigeon[:, :, 1]
# red[:, :] = pigeon[:, :, 2]
blue, green, red = cv2.split(pigeon)

m, n = name.shape
addMatrix = np.zeros(name.shape, dtype=name.dtype)
for i in range(m):
    for j in range(n):
        if name[i, j] < 127:
            addMatrix[i, j] = 1
        else:
            addMatrix[i, j] = 0

m, n = blue.shape
for i in range(m):
    for j in range(n):
        if blue[i, j] % 2 != 0:
            blue[i, j] -= 1
tmp = blue + addMatrix
print tmp
result = cv2.merge([tmp, green, red])
cv2.imwrite("../../outputdata/hw1/result.jpg", result)
print result
hidden = cv2.imread("../../outputdata/hw1/result.jpg")
print hidden
