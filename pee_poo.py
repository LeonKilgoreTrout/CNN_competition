from PIL import Image, ImageOps
import numpy as np
from math import ceil


''' function presented below is able to make an image convolution with tunable stride and filter values
& max/mean/min pooling made by 2/2 filter with stride=2 
so, check it, by using your own image
there are some included filters but you can put yours in
note, that this function converts your image to the gray one
''' 

def conv_n_pool(img_path, kernel='horizontal', stride=1, pooling=False, IMG_SIZE=(150, 100)):
         
    def pixels_from_path(file_path):
         im = Image.open(file_path)
         im = im.resize(IMG_SIZE)
         im = ImageOps.grayscale(im)
         return np.array(im)  
        
    def check_byte(a):
        if a > 255:
            a = 255
        if a < 0:
            a = 0
        return a

    def choose_pooling(bytes_list, state):

        array_1, array_2 = [], []
        for i in range(0, len(bytes_list) - 1, 2):

            for j in range(0, len(bytes_list[0]) - 1, 2):

                if state == 'max':
                    value = max(bytes_list[i][j], bytes_list[i + 1][j], bytes_list[i][j + 1], bytes_list[i + 1][j + 1])
                elif state == 'min':
                    value = min(bytes_list[i][j], bytes_list[i + 1][j], bytes_list[i][j + 1], bytes_list[i + 1][j + 1])
                elif state == 'mean':
                    value = (bytes_list[i][j] + bytes_list[i + 1][j] + bytes_list[i][j + 1] + bytes_list[i + 1][j + 1]) / 4
                else:
                    raise ValueError('Invalid pooling value specified! Use either "mean" or "min" or "max".')
                array_1.append(value)  

            array_2.append(array_1)
            array_1 = []

        return np.array(array_2)
    
    filters = {
    'vertical'       : [[-1, 2, -1],
                        [-1, 2, -1],
                        [1, 2, -1]],
    
    'horizontal'     : [[-1, -1, -1],
                        [2, 2, 2],
                        [-1, -1, -1]],
    
    'central'        : [[-1, -1, -1],
                        [-1, 8, -1],
                        [-1, -1, -1]],
    
    'secondary_diag' : [[-1, -1, 2],
                        [-1, 2, -1],
                        [2, -1, -1]],
    
    'main_diag'      : [[2, -1, -1],
                        [-1, 2, -1],
                        [-1, -1, 2]],
    
    'x_like'         : [[1, -1, 1],
                        [-1, 1, -1],
                        [1, -1, 1]],
    
    'reversed_x'     : [[-1, 1, -1],
                        [1, -1, 1],
                        [-1, 1, -1]]
                }
    
    if isinstance(kernel, list):
        
        try:
            assert len(kernel[0]) == len(kernel)            
        except AssertionError:
            raise ValueError('Invalid kernel value specified! Try one of these:\n"vertical", "horizontal", "central", "secondary_diag", "main_diag", "x_like", "reversed_x" or use your own 2D numeric array')
        
        
        try:
            kernel[0][0]
            for i in kernel:
                for k in kernel:
                    try:
                        assert isinstance(kernel[0][0], int) or isinstance(kernel[0][0], float)
                    except AssertionError:
                        raise ValueError('Invalid kernel value specified! Try one of these:\n"vertical", "horizontal", "central", "secondary_diag", "main_diag", "x_like", "reversed_x" or use your own 2D numeric array')
        except TypeError:
                raise ValueError('Invalid kernel value specified! Try one of these:\n"vertical", "horizontal", "central", "secondary_diag", "main_diag", "x_like", "reversed_x" or use your own 2D numeric array')
        
        fltr = kernel
        
    else:    
        try:
            fltr = filters[kernel]
        except KeyError:
            raise ValueError('Invalid kernel value specified! Try one of these:\n"vertical", "horizontal", "central", "secondary_diag", "main_diag", "x_like", "reversed_x" or use your own 2D numeric array')
    
    rows, cols = len(pixs), len(pixs[0])
    
    length = len(fltr)
    pixs = pixels_from_path(img_path)     
    img_ = []
    for i in range(0, cols + 1 - length, stride):
        sumf = []
        for j in range(0, rows + 1 - length, stride):
            sums = 0
            for x in range(length):
                for s in range(length):
                    sums += pixs[j + x][i + s] * fltr[x][s]
            sumf.append(check_byte(sums))
        img_.append(sumf)

    img_ = np.array(img_).T

    if pooling:
        return choose_pooling(img_, pooling)

    return img_
