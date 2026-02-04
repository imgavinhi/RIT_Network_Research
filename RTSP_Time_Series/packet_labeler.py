def hex_to_ip(hex_str):
    """Converts 8 hex characters into a standard IP address."""
    try:
        return '.'.join(str(int(hex_str[i:i+2], 16)) for i in range(0, 8, 2))
    except:
        return "Unknown"

def packet_types(raw_line_data):
    """
    Identifies RTSP status codes and host IPs.
    Uses a global search to ensure '401' isn't missed by the Labeler.
    """
    packet = "Background"
    traffic_class_int = 0
    hosts = ("Unknown", "Unknown")
    
    # Strip all formatting to ensure string searches work
    clean_hex = raw_line_data.replace("|", "").replace(" ", "").strip()
    
    # Identify IPv4 (Look for EtherType 0800)
    if "0800" in clean_hex[20:32]:
        src_ip = hex_to_ip(clean_hex[52:60])
        dst_ip = hex_to_ip(clean_hex[60:68])
        
        # Check for RTSP Port 554 (Hex: 022a)
        if "022a" in clean_hex[64:84]:
            hosts = (src_ip, dst_ip)
            # Start with Data Transmission as the default RTSP type
            packet = "RTSP_DATA_TRANSMISSION"
            traffic_class_int = 4 
            
            # Search for the RTSP Header (RTSP/1.0 -> 525453502f312e30)
            if "525453502f312e30" in clean_hex:
                # If we find '401' (343031) anywhere in this packet, it's an error
                if "343031" in clean_hex:
                    packet = "CLIENT_ERR_401"
                    traffic_class_int = 2
                # If we find '200' (323030), it's a success
                elif "323030" in clean_hex:
                    packet = "SUCCESS_200"
                    traffic_class_int = 1
                    
    return packet, traffic_class_int, hosts