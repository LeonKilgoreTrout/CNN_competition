import cv2
import numpy as np
from math import ceil

%matplotlib inline

''' this function is able to make an image convolution with tunable stride n filter values
& max/mean/min pooling by 2/2 filter with stride=2 
so, check it, by using your own image
img_link should be string-like
''' 
def conv_pool(img_link,
         filter=[
                 [-1, -1, 3, -1, -1],
                 [-1, -1, 5, -1, -1],
                 [-1, -1, 9, -1, -1],
                 [-1, -1, 5, -1, -1],
                 [-1, -1, 3, -1, -1]
                ],
         stride=1,
         pooling=False
         ):

    def checkByte(a):
        if a > 255:
            a = 255
        if a < 0:
            a = 0
        return a

    def poo(a, state):

        c, k = [], []
        for i in range(0, len(a) - 1, 2):

            for j in range(0, len(a[0]) - 1, 2):

                if state == 'max':
                    xx = max(a[i][j], a[i + 1][j], a[i][j + 1], a[i + 1][j + 1])
                elif state == 'min':
                    xx = min(a[i][j], a[i + 1][j], a[i][j + 1], a[i + 1][j + 1])
                elif state == 'mean':
                    xx = (a[i][j] + a[i + 1][j] + a[i][j + 1] + a[i + 1][j + 1]) / 4
                else:
                    raise ValueError('Invalid pooling value specified! Use either "mean" or "min" or "max".')
                c.append(xx)  

            k.append(c)
            c = []

        return np.array(k)


    obj = cv2.imread(img_link)
    obj = cv2.cvtColor(obj, cv2.COLOR_RGB2GRAY)
    rows, cols = len(obj), len(obj[0])
    length = len(filter)

    sumof = []
    for i in range(0, cols + 1 - length, stride):
        sumf = []
        for j in range(0, rows + 1 - length, stride):
            sums = 0
            for x in range(length):
                for s in range(length):
                    sums += obj[j + x][i + s] * filter[x][s]
            sumf.append(checkByte(sums))
        sumof.append(sumf)

    sumof = np.array(sumof).T

    if pooling:
        return poo(sumof, pooling)

    return sumof
