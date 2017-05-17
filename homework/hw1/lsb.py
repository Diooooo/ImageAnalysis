from PIL import Image
import numpy as np


class lsb:
    def __init__(self, imgPath, namePath):
        self.imgPath = imgPath
        self.namePath = namePath

    def hide(self):
        image = Image.open(self.imgPath)
        name = Image.open(self.namePath).convert('L')

        resultImage = image.copy()

        m, n = name.size

        for i in range(m):
            for j in range(n):
                before = resultImage.getpixel((i, j))
                resultImage.putpixel((i, j), (before[0] - before[0] % 2, before[1], before[2]))
                if name.getpixel((i, j)) < 127:
                    old = resultImage.getpixel((i, j))
                    resultImage.putpixel((i, j), (old[0] + 1, old[1], old[2]))
        print resultImage.split()[0]
        resultImage.save("../../outputdata/hw1/result.jpg")

    def decrypt(self, hiddenPath):
        hidden = Image.open(hiddenPath)
        restoreName = Image.new("L", hidden.size)
        print hidden.split()[0]
        m, n = hidden.size
        for i in range(m):
            for j in range(n):
                if hidden.getpixel((i, j))[0] % 2 == 1:
                    restoreName.putpixel((i, j), 0)
                else:
                    restoreName.putpixel((i, j), 255)
        restoreName.save("../../outputdata/hw1/restore.bmp")


lsb = lsb("../../testdata/hw1/pigeon.jpg", "../../testdata/hw1/name.jpg")
lsb.hide()
lsb.decrypt("../../outputdata/hw1/result.jpg")
