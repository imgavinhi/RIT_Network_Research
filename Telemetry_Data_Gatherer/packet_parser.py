'''
Parses the first x number of bytes from a packet and adds padding if necessary.
'''
import re
import os

# Function to parse packets from a file
def packet_parser(file, byte_count):
    cap_dir = "captures/"
    cap_file = os.path.join(cap_dir, file)
    hex_char_count = int(byte_count) * 2  # Each byte is represented by two hex characters
    byte_list = []
    timestamp_list = []
    
    # Regex to match timestamps (with microseconds)
    timestamp_regex = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"
    
    current_packet_hex = []
    
    with open(cap_file, 'r') as f:
        for line in f:
            # Extract timestamp if it matches the regex pattern
            match = re.search(timestamp_regex, line)
            if match:
                # If there's data from a previous packet, store it before resetting
                if current_packet_hex:
                    # Join hex bytes and add padding if needed
                    hex_data = ''.join(current_packet_hex)[:hex_char_count]
                    if len(hex_data) < hex_char_count:
                        hex_data += '0' * (hex_char_count - len(hex_data))
                    byte_list.append(hex_data)
                    current_packet_hex = []  # Reset for the new packet

                timestamp = match.group(1)
                timestamp_list.append(timestamp)

            # Process hex bytes in the line (those starting with 0x)
            if re.search(r'0x[0-9a-fA-F]{4}', line):
                hex_part = line.split(":")[1].strip()  # Get the hex data part after ':'
                hex_bytes = hex_part.split()           # Split into individual hex bytes
                # Extend current packet hex with valid hex bytes
                current_packet_hex.extend([byte for byte in hex_bytes if re.match(r'^[0-9a-fA-F]+$', byte)])

        # Handle the last packet in the file if it didn't end with a new timestamp
        if current_packet_hex:
            hex_data = ''.join(current_packet_hex)[:hex_char_count]
            if len(hex_data) < hex_char_count:
                hex_data += '0' * (hex_char_count - len(hex_data))
            byte_list.append(hex_data)

    # Write to output file
    wo_extension, extension = os.path.splitext(file)
    new_file = f"{wo_extension}_parsed.txt"

    parsed_dir = "parsed_captures/"
    parsed_file = os.path.join(parsed_dir, new_file)

    
    with open(parsed_file, "w") as n:
        for index, packet in enumerate(byte_list):
            if index < len(timestamp_list):  # Ensure there's a timestamp for each packet
                n.write(f"{timestamp_list[index]}\n")  # Write timestamp
            n.write(packet + "\n")  # Write hex data without spaces

    print(f"File created: {new_file}")

# Example usage
# packet_parser("path_to_your_input_file.txt", 200)

