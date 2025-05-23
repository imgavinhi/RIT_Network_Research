import numpy as np
from datetime import datetime
import time
import os
from packet_labeler import *
from packet_parser import *
import re

timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+'

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
            #WILL HAVE TO REMOVE/SKIP TIMESTAMPS IN PARSED FILE
            if re.match(timestamp_pattern, line):
                continue
            else:
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
            if re.match(timestamp_pattern, line):
                continue
            else:
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
        for j in range(x.shape[0]):
            x_normalized[j,i] = x[j,i] - x_mean #the value of the x_normalized array becomes x's value of the array - the mean of x_sum values
    return x_normalized

'''
This function utilizes packet_labeler.py to assign labels to each type of packet pased on the hex data it is given for a packet

Primarily targets ICMP Echo Request, ICMP Echo Reply, ARP Request, and ARP Reply
'''
def fields_and_labels(x_output_file, y):
    icmp_request_ctr = 0
    icmp_reply_ctr = 0
    arp_request_ctr = 0
    arp_reply_ctr = 0
    ctr = 0
    http_ctr = 0
    tls_ctr = 0
    dns_ctr = 0
    quic_ctr = 0

    with open(x_output_file) as traffic:
        for line in traffic:
            #will need to skip timestamp lines
            if re.match(timestamp_pattern, line):
                continue
            x_line_data = line
            

            packet, traffic_class_int, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr = packet_types(x_line_data, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr)

            traffic_class_int = str(traffic_class_int)
            #print(traffic_class_int) is it seeing the traffic class for reply (YES)
            y[ctr] = traffic_class_int
            ctr += 1

            '''debugging
            if ctr%11 == 0:
                print(traffic_class_int)'''

            packet, x_line_data = "", ""
    
    #troubleshooting y
    #print("The following is what Y consists of:", y[:20])
    print("THIS IS A TEST, IGNORE ME!!!\n","ARP: REQ", arp_request_ctr, "ARP: REP", arp_reply_ctr, "ICMP: REQ", icmp_request_ctr, "ICMP: REP", icmp_reply_ctr, "HTTP", http_ctr, "TLS", tls_ctr, "DNS", dns_ctr, "QUIC", quic_ctr)
    return y

'''
This preprocessor parses captures and then utilizes other functions within this file to construct numpy files based on the features and labels captured 
'''
def preprocessor_main(features, dataset_file_list, cleaned_file_list, x_test_file_list, y_test_file_list):
    x_row = 0
    y_row = 0
    y_cols = 1
    x_cols = features

    for i in range(len(dataset_file_list)):
        x_outfile = dataset_file_list[i]

        packet_parser(x_outfile, features)

    for i in range(len(cleaned_file_list)):
        x_source_file = cleaned_file_list[i]
        print(x_source_file)
        x_features_file = x_test_file_list[i]
        y_labels_file = y_test_file_list[i]

        x_rows, y_rows = num_rows(x_source_file)

        x, y = numpy_x_y(x_rows, x_cols, x_source_file, y_rows, y_cols)

        x_normalized = mean_normalization(x, features)

        y = fields_and_labels(x_source_file, y)

        np.save(y_labels_file, y)
        np.save(x_features_file, x_normalized)


'''
Notes for 10/28/2024:
    1) capture
        training data?
        how many files?
        naming convention (ex: dataset_x.txt)
            will be dumped into a file name list
    2) preprocess 
        remove artifacts, truncate, pad (features = length of packet)
    3) eliminate unknown classes or labels
        known: Both ARPs and both ICMPs (remove the rest and timestamps)
    4) convert to proper data format
        seen: wireshark_parser.py

    Look at pytorch tutorials (python array > numpy array > pytorch array)

    wireshark_parser.py:
        |data_clear| performs preprocessing
        |fields_and_labels| creates ground truth and creates counters to ensure ground truth. Returns the ground truth (y)
        |x_normalize| Divides all values of x by 16. This is done to make data fall within a reasonable (easy to graph) scale
        |numpy_x_y|
        |preprocessor| Creates cleaned x source files to num rows to define how big data structure for numpy is. Uses numpy_x_y to create numpy data structures based on number of rows in a cleaned capture, features and populates them with zeros. Defines y with fields_and_labels. Then saves numpy files (x is now fully populated with correct formats based on cleaned data. It is then taken to be normalized) (y labels are then written directory to the y numpy file and saved). Ultimately saved into numpy x and y feature numpy matrices.

    Think of parsed hex data as a matrix with hex characters by number of packets
    For matrix math this will be transposed (flipped)

    What to do:
        -put captures, parsed, and csv data sets into directories in each file
        -move ml architecture from directory to github/Telemetry_Gatherer
'''
