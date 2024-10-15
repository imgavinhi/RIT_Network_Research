''''
parses the first x number of bytes from a packet
'''
import os
import time
import subprocess

def packet_parser(file, byte_count):
    byte_list = []
    timestamp_list = []
    value = int(byte_count) + 1
#    file_path = os.path.join("Telemetry_Script_Output", "Captures", file)
    with open(file, 'r') as f:
        for line in f:
            if line.strip() and ',' in line:
                timestamp = line.split()[0]
                timestamp_list.append(timestamp)

            if line[0] == "|":
                byte_values = line.strip().split("|")[2:value]
                byte_list.append(byte_values)

    for packet in byte_list:
        while len(packet) < int(byte_count):
            packet.append("00")
    
            input("Press Enter to Continue")
#new_dir = os.path.join("Telemetry_Script_Output", "Parsed_Packet")
#os.makedirs(new_dir, exist_ok=True)

    wo_extension, extension = os.path.splitext(file)
    new_file = str(wo_extension) + "_parsed.txt"
#    file_path = os.path.join(new_dir, new_file)

    print("\nFile has been created: " + new_file + "\n")
    time.sleep(5)
    with open(new_file, "w") as n:
        for index, packet in enumerate(byte_list):
            n.write(timestamp_list[index] + '\n')
            for byte in packet:
                n.write(byte)
            n.write("\n")
