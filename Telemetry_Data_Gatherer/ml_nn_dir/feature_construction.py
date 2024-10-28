import numpy as np
from datetime impotr datetime
import time
import os
from packet_labeler import *

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
This function utilizes packet_labeler.py to assign labels to each type of packet pased on the hex data it is given for a packet

Primarily targets ICMP Echo Request, ICMP Echo Reply, ARP Request, and ARP Reply
'''
def fileds_and_labels(x_output_file, y):
    icmp_request_ctr = 0
    icmp_reply_ctr = 0
    arp_request_ctr = 0
    arp_reply_ctr = 0
    ctr = 0

    with open(x_output_file) as traffic:
        for line in traffic:
            #will need to skip timestamp lines
            x_line_data = line
            l2_type = x_line_data[24:28]

            #ipv4
            if l2_type == '0800':
                packet, traffic_class_int, icmp_request_ctr, icmp_reply_ctr = ipv4_types(x_line_data, icmp_request_ctr, icmp_reply_ctr)
            
            #arp
            if l2_type == "0806":
                packet, traffic_class_int, arp_request_ctr, arp_reply_ctr = arp_labeler(x_line_data, arp_request_ctr, arp_reply_ctr)


            traffic_class_int = str(traffic_class_int)
            y[ctr] = traffic_class_int
            ctr += 1

            packet, x_line_data = "", ""
    return y

