DISCLAIMER:
This script is not OS agnostic! It can only be run in a Linux environment with tcp_dump installed! Additionally, some modules use "sudo" privileges, so you may be prompted to enter in the sudo password for your machine. If you have questions, please contact the owner of this github repository.

Order of operations when not using machine learning aspect:
Capture Packets > Parse Captures > Create Datasets > Generate Summary Statistics

Telemetry_Data_Gatherer:

| telemetry_data.py |
Main application. It calls the rest of the files, supporting packet capture, parsing a packet, converting packet metadata into a csv format for statistical analysis, and, eventually, generating summary statistics

| packet_capture.py |
Captures a number of packets specified by the user. This module utilizers tcp_dump annd the user may be prompted for a sudo user's password because of this. The user will be prompted to enter a valid interface, a valid capture file name, and an integer for a valid packet count. A capture is saved as a txt file in the {captures/} directory.

| packet_parser.py |
Users will be prompted to enter a file from the {captures/} directory. Parses capture txt files and stores into a timestamp, hex formatted txt file within the {parsed_captures/} directory. Prompts users for a byte count and adds additional padding for non-existing bytes.

| packet_metadata.py |
Generates metadata based on parsed txt file. Determines epoch time, delta time, source and destination mac, source and destination IPv4 address, ether type, length, and protocol ID.

| packet_csv.py |
Users will be prompted to enter a file from the {parsed_packets/} directory. Generates data csv with parsed and meta data information. Datasets are located in the {data_sets/} directory. 

| statistics.py |
Users will be prompted to enter a packet from the {data_sets/} directory. Generates summary statistics for parsed data packets including number of packets, packet distribution, average packet length, max packet length, and min packet length.

| packet_labeler.py |
Classifies packets by a traffic class integer for feature construction. Current labels ARP traffic at layer 2 and ICMPv4 traffic at layer 3. 

1 - ARP Request
2 - ARP Reply
3 - ICMP Request
4 - ICMP Reply (currently has issues identifying)

|feature_construction.py|
This module constructs numpy files for features (x) and labels (y) initally populated with blank values. Populates numpy files with information from parsed tcp_dump captures.

| gen_net_model_mlp.py |

| packet_identifier_architecture.py |

| captures (dir) |
Stores tcp_dump captures from a user specified interface as a txt file.

| parsed_captures (dir) |
Stores parsed tcp_dump captures.

| data_sets (dir) |
Stores datasets of parsed tcp_dump captures.

| numpy_files (dir) |

| datasets_conv (dir) |
