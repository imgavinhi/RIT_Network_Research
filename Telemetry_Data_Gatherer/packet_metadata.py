'''
Gathers packet metrics and stores them into lists.

Each list will be gone through in order to concurrently match data with its respective packet.
'''

import time
from datetime import datetime
import csv

def convert_to_epoch(timestamp_list):
    epochs = []
    for datetime_str in timestamp_list:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
        epoch_start = datetime(1970, 1, 1)
        delta = dt - epoch_start
        epochs.append(int(delta.total_seconds() * 1000))    

    return epochs

def make_lists(filename):
    byte_list = []
    timestamp_list = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in range(0, len(lines), 2):
            if line + 1 < len(lines):
                timestamp = lines[line].strip()
                hex_data = lines[line + 1].strip()

                # Debugging output
                #print(f"Timestamp: {timestamp}, Hex Data: {hex_data}")

                byte_list.append(hex_data)
                timestamp_list.append(timestamp)
    
    # Debugging output
    #print(f"Total Timestamps: {len(timestamp_list)}, Total Bytes: {len(byte_list)}")
    print(timestamp_list)
    #print(byte_list)
    return timestamp_list, byte_list

def metadata_lists(timestamp_list, byte_list):
    dst_macs = []
    src_macs = []
    ether_types = []
    src_ips = []
    dst_ips = []
    pids = []
    src_ports = []
    dst_ports = []
    int_timestamps = []
    time_deltas = []

    # Store values into respective metadata list
    for i, packet in enumerate(byte_list):
        dst_mac = packet[0:11]
        src_mac = packet[12:24]
        ether_type = packet[24:27]
        src_ip = packet[49:56]
        dst_ip = packet[36:43]
        pid = packet[45:47]

        if pid in ['11', '06']:
            src_port = packet[65:68]
            dst_port = packet[69:72]
        else:
            src_port = '0000'
            dst_port = '0000'

        # Ensure we have valid timestamps
        if i < len(timestamp_list):
            time_str = timestamp_list[i].strip()

            # Convert timestamp to total milliseconds since epoch
            dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')  # Parse the timestamp
            int_timestamps.append(dt)

            # Calculate time delta since last packet
            if i == 0:
                time_deltas.append(0)  # First packet, no time delta
            else:
                time_delta = int_timestamps[i] - int_timestamps[i - 1]  # Correctly reference previous timestamp
                time_deltas.append(time_delta.total_seconds())

        # Append to metadata lists
        dst_macs.append(dst_mac)
        src_macs.append(src_mac)
        ether_types.append(ether_type)
        src_ips.append(src_ip)
        dst_ips.append(dst_ip)
        pids.append(pid)
        src_ports.append(src_port)
        dst_ports.append(dst_port)

    # Calculate epoch time
    epochs = convert_to_epoch(timestamp_list)
    print(epochs)
    print(time_deltas)

    return int_timestamps, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs

