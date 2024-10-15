'''
utilizing tshark to capture packets and then save them as k12 packets for parsing
'''

import subprocess
import os

def capture_packets(interface, filename, packet_count):
   # new_dir = os.path.join('Telemetry_Script_Output', 'Caputres')
    #os.makedirs(new_dir, exist_ok=True)
    #capture_path = os.path.join(new_dir, filename)
    capture_command = ['tshark', '-i', interface, '-w', filename, '-c', packet_count]
    file = os.path.splitext(filename)[0]
    k12_filename = file + ".k12"
#    k12_path = os.path.join(new_dir, k12_filename)
    convert_command = ['tshark', '-r', filename, '-F', 'k12text', '-w', k12_filename]
    subprocess.run(capture_command)
    subprocess.run(convert_command)

