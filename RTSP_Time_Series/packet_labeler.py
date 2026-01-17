# packet_labeler.py

def packet_types(x_line_data, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr):
    packet = "Background"
    traffic_class_int = 0 # Default: Not RTSP
    
    l2_type = x_line_data[24:28]

    if l2_type == '0800': # IPv4
        l3_pid = x_line_data[46:48] # 06=TCP, 11=UDP
        src_port = x_line_data[68:72]
        dst_port = x_line_data[72:76]

        # RTSP uses Port 554 (Hex: 022a)
        #maybe expand to determine if RTSP streaming is failing or differnet codes present
        if (l3_pid == '06' or l3_pid == '11') and (src_port == '022a' or dst_port == '022a'):
            packet = "RTSP"
            traffic_class_int = 1 # Class 1: RTSP
            
    return packet, traffic_class_int, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr