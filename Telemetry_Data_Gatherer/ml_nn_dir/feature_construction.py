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
    #".zeros" returns a new array of a given "shape" and type, filled with zeros
    #"flipping" the features matrix
    x = np.zeros((x_cols, x_rows)) #array "shape" is a 2D array also matches appropraite size
    y = np.zeros((y_rows, y_cols))

    i = 0

    with open(x_output_file) as traffic:
        for line in traffic:
            for j in range(x_cols):
                x[j][i]=int(line[j], 16) #
            i = i + 1
    '''
    x and y are both 2D Arrays filled with zeroes. 
    x is __ by __
    y is __ by __
    '''
    return x, y

'''
This function provides the mean normalization value for x
feature = the number of features

'''
def mean_normalization(x, features):
    #".shape" returns the shape of an array (in this case 2D array)
    x_normalized = np.zeros((x.shape[0], x.shape[1]))

    for i in range(x.shape[1]):
        #".sum" returns a sum of array elements over a given axis
        x_sum = np.sum(x[:,i]) #x_sum is the sum of x's column of the current iteration
        x_mean = x_sum/features #sum of x's current column divided by the number of features
        for j in range(X.shape[0]):
            x_normalized[j,i] = x[j,i] - x_mean #the value of the x_normalized array becomes x's value of the array - the mean of x_sum values
    return x_normalized

'''

'''
def fileds_and_labels(x_output_file, y):
    pass
