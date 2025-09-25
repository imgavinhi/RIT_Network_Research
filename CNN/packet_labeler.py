'''
this function defines labels for ARP and IPv4 packets. So far it only does ICMP Echo Requests and Echo Replies
utilizes traffic class ints of 1 (arp requests) and 2 (arp replies)
utilizes traffic class ints of 3 (icmp requests) and 4 (icmp replies)
utilizes traffic class ints of 5 (tls) and 6 (http) - TCP header with other identifiers
utilizes traff ints of 7 (dns) and 8 (quic) - UDP header with other identifiers
'''
def packet_types(x_line_data, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr):
    packet = "No Match"
    # Assign a default value for traffic_class_int for all unknown traffic
    traffic_class_int = -1
    
    l2_type = x_line_data[24:28]

    if l2_type == '0806':
        arp_type_code = x_line_data[40:44]
        if arp_type_code == "0001":
            packet = "ARP Echo Request"
            traffic_class_int = 0
            arp_request_ctr = arp_request_ctr + 1
        elif arp_type_code == "0002":
            packet = "ARP Echo Reply"
            traffic_class_int = 1
            arp_reply_ctr = arp_reply_ctr + 1

    elif l2_type == '0800':
        l3_pid = x_line_data[46:48]
        l3_type = x_line_data[24:28]
        
        if l3_type == '0800':
            l3_pid = x_line_data[46:48]
            src_port = x_line_data[68:72]
            dst_port = x_line_data[72:76]

            if l3_pid == '01':
                icmp_type_code = x_line_data[68:72]
                if icmp_type_code == '0800':
                    packet = 'IPv4 ICMP Request'
                    traffic_class_int = 2
                    icmp_request_ctr = icmp_request_ctr+1
                elif icmp_type_code == '0000':
                    packet = 'IPv4 ICMP Reply'
                    traffic_class_int = 3
                    icmp_reply_ctr = icmp_reply_ctr+1

    return packet, traffic_class_int, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr