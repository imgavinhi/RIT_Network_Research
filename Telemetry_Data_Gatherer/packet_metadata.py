''''
gathers packet metrics and stores them into lists

each list will be gone through in order to concurrently to match data with its respective packet
'''
import time

import time
from datetime import datetime, timedelta

from datetime import datetime

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

#INSERT FUNCTION TO GET BYTE_LIST AND TIMESTAMP_LIST FROM TXT FILE
def make_lists(filename):
    byte_list = []
    timestamp_list = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in range(0, len(lines), 2):

            if line + 1 < len(lines):
                timestamp = lines[line].strip()
                hex_data = lines[line+1].strip()

                byte_list.append(hex_data)
                timestamp_list.append(timestamp)
    return timestamp_list, byte_list

def metadata_lists(timestamp_list, byte_list):
#    print(timestamp_list)
#    print(byte_list)
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

    #store values into respective metadata list
    for i,packet in enumerate(byte_list):
        dst_mac = packet[0:11]
        src_mac = packet[12:23]
        ether_type = packet[12:14]
        src_ip = packet[28:35]
        dst_ip = packet[36:43]
        pid = packet[45:46]
        
        if pid == '11' or pid == '06':
            src_port = packet[65:68]
            dst_port = packet[69:72]
        else:
            src_port = '0000'
            dst_port = '0000'
        
        #convert each entry in the timestamp_list to a int
        for t in timestamp_list:
            time = t.strip()
            
            if ',' in time:
                comma_index = time.index(',')
                time_part = time[:comma_index]  # Get the part before the comma
                milliseconds = time[comma_index + 1:]  # Get the part after the comma

                # Remove any commas from the milliseconds part
                milliseconds = milliseconds.replace(',', '')

                hours, minutes, seconds = map(int, time_part.split(':'))
                total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000 + int(milliseconds)
                
                int_timestamps.append(total_milliseconds)
                print(int_timestamps)

        #calculate time delta since last packet
        if i == 0:
            time_deltas.append(0)
        else:
            time_delta = int_timestamps[i] - int_timestamps[i-1]  # Time since last packet
            time_deltas.append(time_delta)

        #append to metadata lists
        dst_macs.append(dst_mac)
        src_macs.append(src_mac)
        ether_types.append(ether_type)
        src_ips.append(src_ip)
        dst_ips.append(dst_ip)
        pids.append(pid)
        src_ports.append(src_port)
        dst_ports.append(dst_port)
    
    #calculate epoch time
    epochs = convert_to_epoch(timestamp_list)

    return int_timestamps, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs

