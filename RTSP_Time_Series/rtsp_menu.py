'''
main function to assist in gather packet statistics
'''
from packet_parser import packet_parser
from feature_construction import *
from gen_net_model_cnn import *
from packet_identifier_architecture import *
from packet_labeler import *


from os import system
import os
import subprocess
import time

def main():
    run = True
    while run:
        system("clear")
        #P = Parse Packet (txt file), Q = Quit program

        print("********RTSP Time Series********\n")
        print("Please select one of the following options:")
        print("\tP: Parse Capture Packet\n\tM: Machine Learning Neural Network\n\tQ: Quit Program")
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
        
            packet_parser(file_location, byte_count)
            input("Parsing complete. Press Enter to Continue...")

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