import cv2
import numpy as np

pigeon = cv2.imread("../../testdata/hw1/pigeon.jpg")
name = cv2.imread("../../testdata/hw1/name.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
print name.shape
print name.dtype
result = pigeon.copy()


print result.shape
grey = cv2.split(name)[0]
m,n = grey.shape
print m, n
count = 0
for i in range(m):
    for j in range(n):
        if grey[i, j] not in [0, 255]:
            count += 1
print count
