# packet_labeler.py

def packet_types(x_line_data):
    """
    Identifies RTSP status codes within a packet to determine stream health.
    Returns: packet_name (string), traffic_class_int (int)
    """
    packet = "Background"
    traffic_class_int = 0 # Default: Non-RTSP or Noise
    
    # Check for IPv4 (Hex: 0800)
    l2_type = x_line_data[24:28]

    if l2_type == '0800': 
        l3_pid = x_line_data[46:48] # 06=TCP, 11=UDP
        src_port = x_line_data[68:72]
        dst_port = x_line_data[72:76]

        # RTSP Port 554 (Hex: 022a)
        if (l3_pid == '06' or l3_pid == '11') and (src_port == '022a' or dst_port == '022a'):
            # Default to general RTSP
            packet = "RTSP_GENERAL"
            traffic_class_int = 1 
            
            # Search for RTSP Response Header: "RTSP/1.0 " (Hex: 525453502f312e3020)
            payload = x_line_data[84:] 
            header_index = payload.find("525453502f312e3020")
            
            if header_index != -1:
                # Extract the 3-digit status code immediately following the header
                # Status code bytes are 6 hex characters long
                code_hex = payload[header_index + 18 : header_index + 24]
                try:
                    # Convert hex back to ASCII (e.g., 323030 -> "200")
                    status_code = bytes.fromhex(code_hex).decode('ascii')
                    
                    if status_code.startswith('2'): # Success (e.g., 200 OK)
                        packet = "RTSP_SUCCESS"
                        traffic_class_int = 1
                    elif status_code.startswith('4'): # Client Error (e.g., 401 Unauthorized)
                        packet = "RTSP_CLIENT_ERR"
                        traffic_class_int = 2
                    elif status_code.startswith('5'): # Server Error (e.g., 500 Internal Error)
                        packet = "RTSP_SERVER_ERR"
                        traffic_class_int = 3
                except:
                    pass
            
    return packet, traffic_class_int