Telemetry_Data_Gatherer:

| telemetry_data.py | 
Main application. It calls the rest of the files, supporting packet capture, parsing a packet, converting packet metadata into a csv format for statistical analysis, and, eventually, generating summary statistics

| packet_capture.py |
Captures a number of packets specified by the user. Capture is saved as a txt file.

| packet_parser.py |
Parses capture txt files and stores into a timestamp, hex formatted txt file.

| packet_metadata.py |
Generates metadata based on parsed txt file. Determines epoch time, delta time, etc.

| packet_csv.py |
Generates data csv with parsed and meta data information.

| statistics.py |
Generates summary statistics for parsed data packets including number of packets, packet distribution, average packet length, max packet length, and min packet length.

| feature_construction.py |

| packet_labeler.py |

| gen_net_model_mlp.py |

| packet_identifier_architecture.py |

| captures (dir) |

| parsed_captures (dir) |

| data_sets (dir) |

| numpy_files (dir) |

| datasets_conv (dir) |
