def hex_to_ip(hex_str):
    """Converts 8 hex characters into a standard IP address."""
    return '.'.join(str(int(hex_str[i:i+2], 16)) for i in range(0, 8, 2))

def packet_types(x_line_data):
    packet = "Background"
    traffic_class_int = 0
    hosts = ("Unknown", "Unknown")
    
    # Identify IPv4 by looking for '0800' (usually starts at index 24)
    if '0800' in x_line_data[20:30]: 
        # Extract IPs: Source is at 52-60, Dest is at 60-68
        src_ip = hex_to_ip(x_line_data[52:60])
        dst_ip = hex_to_ip(x_line_data[60:68])
        
        # Check for RTSP Port 554 (Hex: 022a)
        if '022a' in x_line_data[64:80]: 
            hosts = (src_ip, dst_ip)
            packet = "RTSP_GENERAL"
            traffic_class_int = 1 
            
            # Search the whole line for "RTSP/1.0 " (Hex: 525453502f312e3020)
            payload = x_line_data
            header_index = payload.find("525453502f312e3020")
            
            if header_index != -1:
                # Extract 3-digit status code (6 hex chars)
                code_hex = payload[header_index + 18 : header_index + 24]
                try:
                    status_code = bytes.fromhex(code_hex).decode('ascii')
                    if status_code.startswith('2'): 
                        packet = "RTSP_SUCCESS"; traffic_class_int = 1
                    elif status_code.startswith('4'): # Detects 401 Unauthorized
                        packet = "RTSP_CLIENT_ERR"; traffic_class_int = 2
                    elif status_code.startswith('5'): 
                        packet = "RTSP_SERVER_ERR"; traffic_class_int = 3
                except:
                    pass
            
    return packet, traffic_class_int, hosts