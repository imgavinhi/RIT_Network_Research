'''
utilizing tshark to capture packets and then save them as k12 packets for parsing
'''

import subprocess
import os

def capture_packets(interface, filename, packet_count):
    # Ensure the output directory exists
    # new_dir = os.path.join('Telemetry_Script_Output', 'Captures')
    # os.makedirs(new_dir, exist_ok=True)
    # capture_path = os.path.join(new_dir, filename)

    # Create the tcpdump command
    capture_command = ['sudo', 'tcpdump', '-i', interface, '-c', str(packet_count), '-XX', '-tttt']

    # Open the output file in write mode
    with open(filename, 'w') as f:
        # Run the command and redirect stdout to the file
        subprocess.run(capture_command, stdout=f)

    # Generate the k12 filename
    file = os.path.splitext(filename)[0]
    new_filename = file + ".txt"


