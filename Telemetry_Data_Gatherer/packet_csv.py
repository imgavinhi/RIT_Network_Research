''''
stores packet metadata into a csv file
'''
# csv_writer.py
import csv
import os

def write_to_csv(filename, byte_list, timestamp_list, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs):
    wo_extension, extension = os.path.splitext(filename)
    new_filename = str(wo_extension) + ".csv"
    with open(new_filename, 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Destination MAC', 'Source MAC', 'Ether Type', 'Source IP', 'Destination IP', 'PID', 'Source Port', 'Destination Port', 'Time Delta', 'Epoch']
        

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(byte_list)):
            writer.writerow({
                'Timestamp': timestamp_list[i] if i < len(timestamp_list) else '',
                'Destination MAC': ':'.join(dst_macs[i]),
                'Source MAC': ':'.join(src_macs[i]),
                'Ether Type': ''.join(ether_types[i]),
                'Source IP': '.'.join(src_ips[i]),
                'Destination IP': '.'.join(dst_ips[i]),
                'PID': pids[i],
                'Source Port': ''.join(src_ports[i]),
                'Destination Port': ''.join(dst_ports[i])
#                'Time Delta': time_deltas[i],
#                'Epoch': epochs[i]
            })

