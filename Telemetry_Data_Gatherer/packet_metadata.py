'''
gathers packet metrics and stores them into lists

each list will be gone through in order to concurrently to match data with its respective packet
'''

import time
from datetime import datetime
import csv

def convert_to_epoch(timestamps):
    epochs = []  # List to store the calculated epoch times
    current_date = datetime.now()  # Get the current date

    for seconds_milliseconds in timestamps:
        # Ensure the input is formatted correctly
        if ',' in seconds_milliseconds:
            parts = seconds_milliseconds.split(',')
            if len(parts) == 3:  # Adjust this if your format changes
                time_part = parts[0].strip()  # hh:mm:ss
                milliseconds = int(parts[1].strip()[:3])  # Only take the first 3 digits

                hours, minutes, seconds = map(int, time_part.split(':'))

                # Create a datetime object for the current date with the provided time
                dt = datetime(current_date.year, current_date.month, current_date.day, hours, minutes, seconds, milliseconds * 1000)

                # Calculate the total seconds since the epoch (current date)
                epoch_time = int((dt - datetime(1970, 1, 1)).total_seconds())
                epochs.append(epoch_time)

    # Return the list of epoch times
    return epochs

# INSERT FUNCTION TO GET BYTE_LIST AND TIMESTAMP_LIST FROM TXT FILE
def make_lists(filename):
    byte_list = []
    timestamp_list = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in range(0, len(lines), 2):
            if line + 1 < len(lines):
                timestamp = lines[line].strip()
                hex_data = lines[line + 1].strip()

                byte_list.append(hex_data)
                timestamp_list.append(timestamp)
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
        src_mac = packet[12:23]
        ether_type = packet[12:14]
        src_ip = packet[28:35]
        dst_ip = packet[36:43]
        pid = packet[45:46]

        if pid in ['11', '06']:
            src_port = packet[65:68]
            dst_port = packet[69:72]
        else:
            src_port = '0000'
            dst_port = '0000'

        # Ensure we have valid timestamps and convert each entry in the timestamp_list to an int
        if i < len(timestamp_list):
            time = timestamp_list[i].strip()

            if ',' in time:
                comma_index = time.index(',')
                time_part = time[:comma_index]  # Get the part before the comma
                milliseconds = time[comma_index + 1:].strip()  # Get the part after the comma

                # Remove any commas from the milliseconds part
                milliseconds = milliseconds.replace(',', '')

                hours, minutes, seconds = map(int, time_part.split(':'))
                total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000 + int(milliseconds)

                int_timestamps.append(total_milliseconds)

        # Calculate time delta since last packet
        if len(int_timestamps) > 0:  # Check if we have at least one timestamp
            if i == 0:
                time_deltas.append(0)
            else:
                time_delta = int_timestamps[i - 1] - int_timestamps[i - 2]  # Time since last packet
                time_deltas.append(time_delta)

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

    return int_timestamps, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs

def write_to_csv(filename, byte_list, timestamp_list, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs):
    # Ensure all lists are of the same length
    min_length = min(len(byte_list), len(timestamp_list), len(dst_macs), len(src_macs), len(ether_types), len(src_ips), len(dst_ips), len(pids), len(src_ports), len(dst_ports), len(time_deltas), len(epochs))

    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['Byte Data', 'Timestamp', 'Dst MAC', 'Src MAC', 'Ether Type', 'Src IP', 'Dst IP', 'PID', 'Src Port', 'Dst Port', 'Time Delta', 'Epoch']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(min_length):
            writer.writerow({
                'Byte Data': byte_list[i],
                'Timestamp': timestamp_list[i],
                'Dst MAC': dst_macs[i],
                'Src MAC': src_macs[i],
                'Ether Type': ether_types[i],
                'Src IP': src_ips[i],
                'Dst IP': dst_ips[i],
                'PID': pids[i],
                'Src Port': src_ports[i],
                'Dst Port': dst_ports[i],
                'Time Delta': time_deltas[i],
                'Epoch': epochs[i]
            })

# Example usage:
# filename = "your_packet_data_file.txt"
# timestamp_list, byte_list = make_lists(filename)
# int_timestamps, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs = metadata_lists(timestamp_list, byte_list)
# write_to_csv("output.csv", byte_list, timestamp_list, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs)

