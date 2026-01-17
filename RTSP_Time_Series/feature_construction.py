import numpy as np
from datetime import datetime
import time
import os
from packet_labeler import *
from packet_parser import *
import re

# Regex to skip timestamp lines in parsed files
timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+'

def num_rows(filename):
    """
    Counts the total number of packets in the parsed file by skipping timestamps.
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
    """
    Constructs a 4D NumPy array where each sample is a 12x148 'image' of a packet sequence.
    Also extracts the host IP addresses for each conversation.
    """
    total_packets = x_rows
    # Grouping packets into conversations (Time Series)
    num_samples = total_packets // packet_height
    
    # X shape: (samples, 1, height, width)
    x = np.zeros((num_samples, 1, packet_height, packet_width), dtype=np.float32)
    # Y shape: (samples, 1) - One label applied to the entire time series
    y = np.zeros((num_samples, 1), dtype=np.int32)
    host_list = [] # Map conversation index to (Src_IP, Dst_IP)

    with open(x_output_file) as traffic:
        # Filtering out timestamps to get raw hex lines
        lines = [line.strip() for line in traffic if not re.match(timestamp_pattern, line)]
        
        for i in range(num_samples):
            # Define the current 12-packet window/conversation
            start_pkt = i * packet_height
            end_pkt = start_pkt + packet_height
            sequence_lines = lines[start_pkt : end_pkt]
            
            # Labeling priority: if any packet in the sequence is an error, the whole sequence is an error
            highest_priority_label = 0
            # Identify hosts from the first valid RTSP packet found in the window
            conv_hosts = ("Unknown", "Unknown")
            
            for time_step, line in enumerate(sequence_lines):
                # Populate the 12x148 matrix
                for j in range(min(len(line), packet_width)):
                     x[i, 0, time_step, j] = int(line[j], 16)
                
                # Unpack Name, ID, and Host IPs from the updated labeler
                _, label_id, current_hosts = packet_types(line)
                
                # Update conv_hosts if RTSP traffic is detected and hosts are currently Unknown
                if label_id > 0 and conv_hosts == ("Unknown", "Unknown"):
                    conv_hosts = current_hosts
                
                # Priority: Errors (4xx/5xx) override Success (2xx) or Background
                if label_id > highest_priority_label:
                    highest_priority_label = label_id
            
            y[i, 0] = highest_priority_label
            host_list.append(conv_hosts)
            
    return x, y, np.array(host_list)

def mean_normalization(x):
    """
    Standardizes input data for better CNN convergence.
    """
    x_mean = np.mean(x)
    x_std = np.std(x)
    if x_std == 0:
        return x - x_mean
    x_normalized = (x - x_mean) / x_std
    return x_normalized

def preprocessor_main(features, dataset_file_list, cleaned_file_list, x_test_file_list, y_test_file_list, packet_height, packet_width):
    """
    Main driver to convert raw captures into time-series matrices and host reports.
    """
    y_cols = 1
    x_cols = features

    # Step 1: Parse raw data into cleaned hex strings
    for i in range(len(dataset_file_list)):
        x_outfile = dataset_file_list[i]
        packet_parser(x_outfile, features)

    # Step 2: Structure data into Time Series NumPy arrays
    for i in range(len(cleaned_file_list)):
        x_source_file = cleaned_file_list[i]
        x_features_file = x_test_file_list[i]
        y_labels_file = y_test_file_list[i]
        
        # Construct path for the hosts file mapping
        hosts_file = x_test_file_list[i].replace("features.npy", "hosts.npy")

        x_rows, y_rows = num_rows(x_source_file)

        # Build the 12x148 matrices and extract host IPs
        x, y, hosts = numpy_x_y(x_rows, x_cols, x_source_file, y_rows, y_cols, packet_height, packet_width)

        x_normalized = mean_normalization(x)

        # Save finalized datasets
        np.save(y_labels_file, y)
        np.save(x_features_file, x_normalized)
        np.save(hosts_file, hosts) 
        print(f"Time Series and Host data saved for: {x_source_file}")