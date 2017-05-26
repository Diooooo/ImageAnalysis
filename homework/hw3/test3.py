import numpy as np
import cv2
from matplotlib import pyplot

img = cv2.imread('../../testdata/hw3/hw3.bmp')
edges = cv2.Canny(img, 10, 20)
cv2.imshow("hw3", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()