'''
This file will provide labels based on the l2_type of the ipv4 packet
'''

'''
this function defines labels for IPv4 packets. So far it only does ICMP Echo Requests and Echo Replies
utilizes traffic class ints of 3 (icmp requests) and 4 (icmp replies)
utilizes traffic class ints of 5 (tls) and 6 (http) - TCP header with other identifiers
utilizes traff ints of 7 (dns) and 8 (quic) - UDP header with other identifiers
'''
def ipv4_types(x_line_data, icmp_request_ctr, icmp_reply_ctr):
#    traffic_class_int = 0
    packet = "No Match"
    l3_pid = x_line_data[46:48]
    l3_type = x_line_data[24:28] #located in the ethernet header specifies IPv4
    
    '''
    tesing to make sure ICMP Echo request are properly parsed (they are)
    print(x_line_data)
    print(l3_pid)
    input("stop")
    '''

    #PID: 01 for ICMP, 11 for UDP, 06 for TCP, 02 for IGMP

    if l3_type == '0800':
        l3_pid = x_line_data[46:48]
        src_port = x_line_data[:]
        dst_port = x_line_data[:]
        if l3_pid == '01': #ICMP l3 pid
            icmp_type_code = x_line_data[68:72]
        
            #request type/code = 0800
            #reply type/code = 0000
            if icmp_type_code == '0800':
                packet = 'IPv4 ICMP Request'
                traffic_class_int = 2
                icmp_request_ctr = icmp_request_ctr+1
            elif icmp_type_code == '0000':
                packet = 'IPv4 ICMP Reply'
                traffic_class_int = 3
                icmp_reply_ctr = icmp_reply_ctr+1
        #print("Req: ", icmp_request_ctr, " Rep: ", icmp_reply_ctr) tesing
        #print(traffic_class_int)

        elif l3_pid == '': #TCP l3 pid
            #http and tls
            pass

        elif l3_pid == '11': #UDP l3 pid
            #dns (port 53) and quic (ports 80 and 443)
            pass

    return packet, traffic_class_int, icmp_request_ctr, icmp_reply_ctr

#this function defines labels for ARP packets
#utilizes traffic class ints of 1 and 2
def arp_labeler(x_line_data, arp_request_ctr, arp_reply_ctr):
   # traffic_class_int = 0
    packet = "No Match"
    l2_type = x_line_data[24:28]
    if l2_type == "0806":
        arp_type_code = x_line_data[40:44] #double check when running
        #print("ARP:", arp_type_code)
        if arp_type_code == "0001":
            packet = "ARP Echo Request"
            traffic_class_int = 0
            arp_request_ctr = arp_request_ctr + 1
        elif arp_type_code == "0002":
            packet = "ARP Echo Reply"
            traffic_class_int = 1
            arp_reply_ctr = arp_reply_ctr + 1
    return packet, traffic_class_int, arp_request_ctr, arp_reply_ctr

