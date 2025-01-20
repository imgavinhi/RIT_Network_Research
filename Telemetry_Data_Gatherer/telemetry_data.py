'''
main function to assist in gather packet statistics

combines packet_csv, packet_metadata, and packet_parser
'''
from packet_parser import packet_parser
from packet_csv import write_to_csv
import packet_metadata
from packet_capture import capture_packets
from statistics import statistics
from feature_construction import *
from gen_net_model_mlp import *
from packet_identifier_architecture import *
from packet_labeler import *


from os import system
import os
import subprocess
import time

def main():
    run = True
    current_dir = subprocess.run("pwd")
    parsed_dir = os.path.join("Telemetry_Script_Output", "Parsed_Packets")
    while run:
        system("clear")
        #C = Capture, P = Parse Packet (txt file), D = Create Dataset (csv file), S = Capture Stats, Q = Quit program, L = List Parsed

        print("********TELEMETRY DATA GATHERING SCRIPT********\n")
        print("Please select one of the following options:")
        print("\tP: Parse Capture Packet\n\tD: Create Dataset in CSV format\n\tC: Capture Packets\n\tS: View Capture Statistics\n\tM: Machine Learning Neural Network\n\tQ: Quit Program")
        command = input("\nPlease select a choice: ")
        command = command.upper()
        if command == "P":
            
            while True:
                file_location = input("Please specify the capture name (txt files located in captures/ only): ")
                full_path = os.path.join("captures/", file_location)

                if os.path.isfile(full_path) and full_path.endswith(".txt"):
                    break
                else:
                    print("Error: The file must be a '.txt' file located in the '{capture/}' directory")

            while True:
                try:
                    byte_count = input("Please specify the number of bytes you want from the packet: ")
                    if int(byte_count) > 0:
                        break
                    else:
                        print("Error: Byte Count must be a positive integer.")
                except ValueError:
                    print("Error: Please input a valid integer.")
        
            #have to change this so it is not stored in variables here, instead in a file that you read through to determine values
            packet_parser(file_location, byte_count)

            #int_timestamps, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs = metadata_lists(byte_list, timestamp_list)
            #write_to_csv(byte_list, timestamp_list, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs)
        elif command == "D":
            filename = input("Please enter parsed text file name: ")
            parsed_dir = "parsed_captures/"
            parsed_file = os.path.join(parsed_dir, filename)
            timestamp_list, byte_list = packet_metadata.make_lists(parsed_file)
            int_timestamps, dst_macs, src_macs, ether_types, total_len, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs = packet_metadata.metadata_lists(timestamp_list, byte_list)
            write_to_csv(filename, byte_list, timestamp_list, dst_macs, src_macs, ether_types, total_len, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs)

        elif command == "C":
            #display interfaces
            system("netstat -i")

            try:
                interfaces_output = subprocess.check_output("ip -o link show| awk -F': ' '{print $2}'", shell=True, text=True)
                available_interfaces = interfaces_output.strip().split("\n")
            except subprocess.CalledProcessError:
                print("Error: unable to retrieve network interfaces")
                return

            #validating user interface selection
            while True:
                interface = input("\nPlease specify an interface to capture on: ")
                if interface in available_interfaces:
                    break
                else:
                    print(f"Error: '{interface}' is not a valid interface. Please select from the available interfaces.")

            #validate that user is specifying a txt file
            while True:
                filename = input("Please specify a capture filename (must be txt file): ")
                if filename.endswith(".txt"):
                    break
                else:
                    print("Error: File must end with a '.txt' extension")

            packet_count = input("Please specify the amount of packets to capture: ")
            capture_packets(interface, filename, packet_count)
        elif command == "S":
            csv_file = input("Please specify CSV data file: ")
            statistics(csv_file)
            input("Press Enter to Continue.")
        elif command == "M":
            model_main()
            input("Press Enter to Continue...")
        elif command == "Q":
            print("Quitting Telemtry Data Gathering Script...")
            run = False
        else:
            print("Please enter a valid input.")

if __name__ == '__main__':
    main()
