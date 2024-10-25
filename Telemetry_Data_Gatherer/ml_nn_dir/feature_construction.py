import numpy as np
from datetime impotr datetime
import time
import os

'''
This function...

x is defined as...

y is defined as...

input has to be parsed file resulting from packet_parser.py
'''
def num_rows(filename):
    x_rows = 0
    y_rows = 0

    with open(filename) as data:
        for line in data:
            #WILL PROBABLY HAVE TO REMOVE/SKIP TIMESTAMPS IN PARSED FILE
            x_rows = x_rows+1
            y_rows =y_rows+1
    return x_rows, y_rows

'''
This function...

x_rows =

x_cols =

y_rows =

y_cols =

x_output_file =
'''
def numpy_x_y(x_rows, x_cols, x_output_file, y_rows, y_cols):
    #"flipping" the features matrix
    x = np.zeroes((x_cols, x_rows))
    y = np.zeroes((y_rows, y_cols))

    i = 0

    with open(x_output_file) as traffic:
        for line in traffic:
            for j in range(x_cols):
                x[j][i]=int(line[j], 16) #
            i = i + 1
    return x, y



