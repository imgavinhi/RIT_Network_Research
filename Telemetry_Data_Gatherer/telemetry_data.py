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
        print("\tC: Capture Packets\n\tP: Parse Capture Packet\n\tD: Create Dataset in CSV format\n\tS: View Capture Statistics\n\tM: Machine Learning Neural Network\n\tQ: Quit Program")
        command = input("\nPlease select a choice: ")
        command = command.upper()
        if command == "P":
            print("Captures:")
            system("ls captures/")
            while True:
                file_location = input("\nPlease specify the capture name (txt files located in captures/ only): ")
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
            input("Parsing complete. Press Enter to Continue...")

            #int_timestamps, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs = metadata_lists(byte_list, timestamp_list)
            #write_to_csv(byte_list, timestamp_list, dst_macs, src_macs, ether_types, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs)
        elif command == "D":
            print("Parsed Captures:")
            system("ls parsed_captures/")

            while True:
                filename = input("\nPlease enter parsed text file name: ")
                parsed_dir = "parsed_captures/"
                parsed_file = os.path.join(parsed_dir, filename)
                if os.path.isfile(parsed_file) and parsed_file.endswith(".txt"):
                    break
                else:
                    print("Error: File must be a '.txt' field located in the '{parsed_captures/}'directory")

            timestamp_list, byte_list = packet_metadata.make_lists(parsed_file)
            int_timestamps, dst_macs, src_macs, ether_types, total_len, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs = packet_metadata.metadata_lists(timestamp_list, byte_list)
            write_to_csv(filename, byte_list, timestamp_list, dst_macs, src_macs, ether_types, total_len, src_ips, dst_ips, pids, src_ports, dst_ports, time_deltas, epochs)
            input("Dataset generated. Press Enter to Continue...")

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
            input("Capture Complete. Press Enter to Continue...")

        elif command == "S":
            print("Datasets:")
            system("ls data_sets/")

            while True:
                csv_file = input("\nPlease specify CSV data file: ")
                full_path = os.path.join("data_sets/", csv_file)

                if os.path.isfile(full_path) and full_path.endswith(".csv"):
                    break
                else:
                    print("Error: File must be '.csv' file and located in the '{data_sets}' directory")
            
            statistics(csv_file)
            input("\nPress Enter to Continue.")

        elif command == "M":
            model_main()
            input("\nPress Enter to Continue...")
        elif command == "Q":
            print("Quitting Telemtry Data Gathering Script...")
            run = False
        else:
            print("Please enter a valid input.")

if __name__ == '__main__':
    main()
