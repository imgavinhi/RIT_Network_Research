''''
parses the first x number of bytes from a packet
'''
import re
import os


#EDIT TO ADD PADDING WHEN USER SPECIFIES A BYTE COUNT HIGHER THAN WHAT THE PACKET HAS
def packet_parser(file, byte_count):
    hex_char_count = int(byte_count) * 2  # Each byte is represented by two hex characters
    byte_list = []
    timestamp_list = []
    
    # Regex to match timestamps (with microseconds)
    timestamp_regex = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"
    
    current_packet_hex = []
    
    with open(file, 'r') as f:
        for line in f:
            # Extract timestamp if it matches the regex pattern
            match = re.search(timestamp_regex, line)
            if match:
                timestamp = match.group(1)
                timestamp_list.append(timestamp)
                # Reset for new packet
                current_packet_hex = []
            
            # Extract hex bytes from the lines that have hex data (those starting with 0x)
            if re.search(r'0x[0-9a-fA-F]{4}', line):
                hex_part = line.split(":")[1].strip()  # Get the hex data part after ':'
                hex_bytes = hex_part.split()           # Split into individual hex bytes
                # Extend current packet hex while filtering out non-hex characters
                current_packet_hex.extend([byte for byte in hex_bytes if re.match(r'^[0-9a-fA-F]+$', byte)])
                
                # If we've collected enough hex characters, store them
                if len(current_packet_hex) * 2 >= hex_char_count:
                    # Join the hex bytes and limit to the required number of characters
                    hex_data = ''.join(current_packet_hex)[:hex_char_count]
                    # If fewer bytes are collected than requested, pad with zeros
                    if len(hex_data) < hex_char_count:
                        hex_data += '0' * (hex_char_count - len(hex_data))
                    byte_list.append(hex_data)
                    current_packet_hex = []  # Reset for the next packet

    # Write to output file
    wo_extension, extension = os.path.splitext(file)
    new_file = f"{wo_extension}_parsed.txt"
    
    with open(new_file, "w") as n:
        for index, packet in enumerate(byte_list):
            if index < len(timestamp_list):  # Ensure there's a timestamp for each packet
                n.write(f"{timestamp_list[index]}\n")  # Write timestamp
            n.write(packet + "\n")  # Write hex data without spaces

    print(f"File created: {new_file}")

# Example usage:
# packet_parser("your_packet_dump_file.txt", 32)  # Parses the first 32 hex chars
