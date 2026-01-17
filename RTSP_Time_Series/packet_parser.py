import re
import os

# Function to parse packets from a file
def packet_parser(file, byte_count):
    # Adjust directories as per your local setup
    cap_dir = "captures/"
    cap_file = os.path.join(cap_dir, file)
    hex_char_count = int(byte_count) * 2  # Each byte is represented by two hex characters
    byte_list = []
    timestamp_list = []
    
    # Updated Regex to match timestamps like 18:52:11,441,786
    timestamp_regex = r"(\d{2}:\d{2}:\d{2},\d{3},\d{3})"
    
    current_packet_hex = []
    
    # Ensure the input file exists before opening
    if not os.path.exists(cap_file):
        print(f"Error: {cap_file} not found.")
        return

    with open(cap_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Extract timestamp if it matches the regex pattern
            match = re.search(timestamp_regex, line)
            if match:
                # If there's data from a previous packet, store it before resetting
                if current_packet_hex:
                    hex_data = ''.join(current_packet_hex)[:hex_char_count]
                    if len(hex_data) < hex_char_count:
                        hex_data += '0' * (hex_char_count - len(hex_data))
                    byte_list.append(hex_data)
                    current_packet_hex = []

                # Format timestamp to match output: YYYY-MM-DD HH:MM:SS.uuuuuu
                # Note: Prepending 2024-11-20 as seen in your target output file
                raw_ts = match.group(1).replace(',', '.')
                formatted_ts = f"2024-11-20 {raw_ts}"
                timestamp_list.append(formatted_ts)

            # Process lines starting with '|' containing hex data
            elif line.startswith('|'):
                # Split by '|' and filter out the empty strings and the offset (first column)
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) > 1:
                    # parts[0] is the offset (e.g., '0'), the rest are hex bytes
                    hex_bytes = parts[1:]
                    current_packet_hex.extend(hex_bytes)

        # Handle the last packet in the file
        if current_packet_hex:
            hex_data = ''.join(current_packet_hex)[:hex_char_count]
            if len(hex_data) < hex_char_count:
                hex_data += '0' * (hex_char_count - len(hex_data))
            byte_list.append(hex_data)

    # Write to output file
    wo_extension, extension = os.path.splitext(file)
    new_file = f"{wo_extension}_parsed.txt"

    parsed_dir = "parsed_captures/"
    if not os.path.exists(parsed_dir):
        os.makedirs(parsed_dir)
        
    parsed_file = os.path.join(parsed_dir, new_file)
    
    with open(parsed_file, "w") as n:
        for index, packet in enumerate(byte_list):
            if index < len(timestamp_list):
                n.write(f"{timestamp_list[index]}\n")
                n.write(f"{packet}\n")

#packet_parser('w_dataset0.txt', 128)