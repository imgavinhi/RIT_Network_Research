'''
This file will provide labels based on the l2_type of the ipv4 packet
'''

def ipv4_types(x_line_data, icmp_request_ctr, icmp_reply_ctr):
    traffic_class_int = 0
    packet = "No Match"
    l3_pid = x_line_data[46:48]

    #01 for ICMP, 11 for UDP, 06 for TCP, 02 for IGMP

    if l3_pid == '01':
        icmp_type_code = x_line_data[68:72]
        
        #request type/code = 0800
        #reply type/code = 0000
        if icmp_type_code == '0800':
            packet = 'IPv4 ICMP Request'
            traffic_class_int = 1
            icmp_request_ctr = icmp_request_ctr+1
        if icmp_type_code == '0000'
            packet = 'IPv4 ICMP Reply'
            traffic_class_int = 2
            icmp_reply_ctr = icmp_reply_ctr+1
    return packet, traffic_int_class, icmp_request_ctr, icmp_reply_ctr
