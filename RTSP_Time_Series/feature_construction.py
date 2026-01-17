import numpy as np
from datetime import datetime
import time
import os
from packet_labeler import *
from packet_parser import *
import re

# Regex to skip timestamp lines in parsed files [cite: 15]
timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+'

def num_rows(filename):
    """
    Counts the total number of packets in the parsed file by skipping timestamps. [cite: 15]
    """
    x_rows = 0
    y_rows = 0

    with open(filename) as data:
        for line in data:
            if re.match(timestamp_pattern, line):
                continue
            else:
                x_rows = x_rows + 1
                y_rows = y_rows + 1
    return x_rows, y_rows

def numpy_x_y(x_rows, x_cols, x_output_file, y_rows, y_cols, packet_height, packet_width):
    # Dummy counters
    a, b, c, d, e, f, g, h, i = 0, 0, 0, 0, 0, 0, 0, 0, 0
    total_packets = x_rows
    num_samples = total_packets // packet_height
    
    x = np.zeros((num_samples, 1, packet_height, packet_width), dtype=np.float32)
    y = np.zeros((num_samples, 1), dtype=np.int32)

    with open(x_output_file) as traffic:
        lines = [line.strip() for line in traffic if not re.match(timestamp_pattern, line)]
        
        for i in range(num_samples):
            start_pkt = i * packet_height
            end_pkt = start_pkt + packet_height
            sequence_lines = lines[start_pkt : end_pkt]
            
            highest_priority_label = 0
            
            for time_step, line in enumerate(sequence_lines):
                # Populate matrix
                for j in range(min(len(line), packet_width)):
                     x[i, 0, time_step, j] = int(line[j], 16)
                
                # Scan EVERY packet in the window for a status code
                _, label_id, a,b,c,d,e,f,g,h,i = packet_types(line, a,b,c,d,e,f,g,h,i)
                
                # Priority: Errors (2, 3) override Success (1) or Background (0)
                if label_id > highest_priority_label:
                    highest_priority_label = label_id
            
            y[i, 0] = highest_priority_label
            
    return x, y

def mean_normalization(x):
    """
    Standardizes input data to improve CNN training efficiency. [cite: 23]
    """
    x_mean = np.mean(x)
    x_std = np.std(x)
    if x_std == 0:
        return x - x_mean
    x_normalized = (x - x_mean) / x_std
    return x_normalized

def preprocessor_main(features, dataset_file_list, cleaned_file_list, x_test_file_list, y_test_file_list, packet_height, packet_width):
    """
    Main driver to convert raw captures into time-series matrices for training. [cite: 5, 22]
    """
    y_cols = 1
    x_cols = features

    # Step 1: Parse raw data into cleaned hex strings [cite: 15]
    for i in range(len(dataset_file_list)):
        x_outfile = dataset_file_list[i]
        packet_parser(x_outfile, features)

    # Step 2: Structure data into Time Series NumPy arrays [cite: 10, 22]
    for i in range(len(cleaned_file_list)):
        x_source_file = cleaned_file_list[i]
        x_features_file = x_test_file_list[i]
        y_labels_file = y_test_file_list[i]

        x_rows, y_rows = num_rows(x_source_file)

        # Call numpy_x_y to build the 26x148 matrices [cite: 28]
        x, y = numpy_x_y(x_rows, x_cols, x_source_file, y_rows, y_cols, packet_height, packet_width)

        x_normalized = mean_normalization(x)

        # Save the finalized time-series datasets [cite: 16]
        np.save(y_labels_file, y)
        np.save(x_features_file, x_normalized)
        print(f"Time-series dataset saved: {x_features_file}")