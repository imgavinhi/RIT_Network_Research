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

"""
This function creates and populates a 4D NumPy array for a CNN.

    Params:
        x_rows (int): The number of packets (samples).
        x_cols (int): The number of features (bytes) per packet.
        x_output_file (str): The path to the file containing the parsed packet data.
        y_rows (int): The number of labels.
        y_cols (int): The number of columns for labels (1).
        packet_height (int): The height of the packet 'image'.
        packet_width (int): The width of the packet 'image'.
        
    Returns:
        tuple: A tuple containing the 4D feature array (x) and the 2D label array (y).
"""
def numpy_x_y(x_rows, x_cols, x_output_file, y_rows, y_cols, packet_height, packet_width):
    # Check if the dimensions are valid for reshaping
    if packet_height * packet_width != x_cols:
        raise ValueError("packet_height * packet_width must equal x_cols")

    # Initialize the 4D feature array for the CNN
    # Shape is (samples, channels, height, width)
    x = np.zeros((x_rows, 1, packet_height, packet_width), dtype=np.float32)
    y = np.zeros((y_rows, y_cols), dtype=np.int32)

    i = 0
    with open(x_output_file) as traffic:
        for line in traffic:
            if re.match(timestamp_pattern, line):
                continue
            else:
                for j in range(x_cols):
                    # Calculate the row and column in the 2D 'image'
                    row = j // packet_width
                    col = j % packet_width
                    
                    # Populate the 4D array
                    x[i, 0, row, col] = int(line[j], 16)
                i += 1
    
    return x, y

'''
 Performs mean normalization and standard deviation scaling on a 4D array.
'''
def mean_normalization(x):
    x_mean = np.mean(x)
    x_std = np.std(x)
    x_normalized = (x - x_mean) / x_std
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
def preprocessor_main(features, dataset_file_list, cleaned_file_list, x_test_file_list, y_test_file_list, packet_height, packet_width):
    """
    This preprocessor parses captures and then utilizes other functions within this file to construct numpy files based on the features and labels captured.
    """
    x_row = 0
    y_row = 0
    y_cols = 1
    x_cols = features
    
    # The packet_height and packet_width are now taken as arguments

    for i in range(len(dataset_file_list)):
        x_outfile = dataset_file_list[i]
        packet_parser(x_outfile, features)

    for i in range(len(cleaned_file_list)):
        x_source_file = cleaned_file_list[i]
        print(x_source_file)
        x_features_file = x_test_file_list[i]
        y_labels_file = y_test_file_list[i]

        x_rows, y_rows = num_rows(x_source_file)

        # The function call now includes the new dimensions
        x, y = numpy_x_y(x_rows, x_cols, x_source_file, y_rows, y_cols, packet_height, packet_width)

        x_normalized = mean_normalization(x)

        y = fields_and_labels(x_source_file, y)

        np.save(y_labels_file, y)
        np.save(x_features_file, x_normalized)
