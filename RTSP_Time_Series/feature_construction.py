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
    with open(filename) as data:
        for line in data:
            if re.match(timestamp_pattern, line):
                continue
            else:
                x_rows += 1
    return x_rows, x_rows

def numpy_x_y(x_rows, x_cols, x_output_file, y_rows, y_cols, packet_height, packet_width):
    """
    Constructs a 4D NumPy array where each sample is a 12x148 'image'.
    Implemented strict locking priority to prevent errors being overwritten by data.
    """
    total_packets = x_rows
    num_samples = total_packets // packet_height
    
    # X shape: (samples, 1, height, width)
    x = np.zeros((num_samples, 1, packet_height, packet_width), dtype=np.float32)
    # Y shape: (samples, 1)
    y = np.zeros((num_samples, 1), dtype=np.int32)
    host_list = [] # Map conversation index to (Src_IP, Dst_IP)

    with open(x_output_file) as traffic:
        # Filtering out timestamps to get raw hex lines
        lines = [line.strip() for line in traffic if not re.match(timestamp_pattern, line)]
        
        for i in range(num_samples):
            # Define the current window/conversation 
            start_pkt = i * packet_height
            end_pkt = start_pkt + packet_height
            sequence_lines = lines[start_pkt : end_pkt]
            
            # Initialize state for this 12-packet window
            conversation_label = 0
            conv_hosts = ("Unknown", "Unknown")
            
            for time_step, raw_line in enumerate(sequence_lines):
                # --- DEEP CLEANING FOR MATRIX POPULATION ---
                # Remove pipes and spaces to ensure nibbles are at correct indices
                clean_line = raw_line.replace("|", "").replace(" ", "")
                
                # Populate the 12x148 matrix nibble by nibble
                for j in range(min(len(clean_line), packet_width)):
                     x[i, 0, time_step, j] = int(clean_line[j], 16)
                
                # Unpack label and hosts using the updated global-search labeler
                _, label_id, current_hosts = packet_types(raw_line)
                
                # Capture host IPs persistently once identified
                if current_hosts != ("Unknown", "Unknown"):
                    conv_hosts = current_hosts
                
                # --- STRICT LOCKING PRIORITY ---
                # 1. If we find an error (2 or 3), LOCK it. It cannot be changed.
                if label_id in [2, 3]:
                    conversation_label = label_id
                # 2. If it's data (4), only assign if we haven't found an error yet.
                elif label_id == 4 and conversation_label not in [2, 3]:
                    conversation_label = label_id
                # 3. If it's success (1), only assign if it's currently background (0).
                elif label_id == 1 and conversation_label == 0:
                    conversation_label = label_id
            
            y[i, 0] = conversation_label
            host_list.append(conv_hosts)
            
            # Diagnostic for the user
            print(f"DEBUG: Window {i} | Assigned Ground Truth: {y[i, 0]} | IPs: {conv_hosts}")
            
    return x, y, np.array(host_list)

def mean_normalization(x):
    """Standardizes input data for better CNN convergence."""
    x_mean = np.mean(x)
    x_std = np.std(x)
    if x_std == 0:
        return x - x_mean
    return (x - x_mean) / x_std

def preprocessor_main(features, dataset_file_list, cleaned_file_list, x_test_file_list, y_test_file_list, packet_height, packet_width):
    """Main driver to convert raw captures into time-series matrices and host reports."""
    # Step 1: Parse raw data into cleaned hex strings
    for i in range(len(dataset_file_list)):
        packet_parser(dataset_file_list[i], features)

    # Step 2: Structure data into Time Series NumPy arrays
    for i in range(len(cleaned_file_list)):
        hosts_file = x_test_file_list[i].replace("features.npy", "hosts.npy")
        x_rows, y_rows = num_rows(cleaned_file_list[i])

        # Build the 12x148 matrices and extract hosts
        x, y, hosts = numpy_x_y(x_rows, features, cleaned_file_list[i], y_rows, 1, packet_height, packet_width)

        # Normalize features
        x_normalized = mean_normalization(x)

        # Save finalized datasets
        np.save(y_test_file_list[i], y)
        np.save(x_test_file_list[i], x_normalized)
        np.save(hosts_file, hosts) 
        print(f"Completed Processing: {cleaned_file_list[i]}")