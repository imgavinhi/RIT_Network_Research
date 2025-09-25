'''
this function defines labels for ARP and IPv4 packets. So far it only does ICMP Echo Requests and Echo Replies
utilizes traffic class ints of 0 (arp requests) and 1 (arp replies)
utilizes traffic class ints of 2 (icmp requests) and 3 (icmp replies)
utilizes traffic class ints of 4 (tls) and 5 (http) - TCP header with other identifiers
utilizes traff ints of 6 (dns) and 7 (quic) - UDP header with other identifiers
'''
def packet_types(x_line_data, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr):
    packet = "No Match"
    # Assign a default value for traffic_class_int
    traffic_class_int = -1
    
    l2_type = x_line_data[24:28]

    if l2_type == '0806':
        arp_type_code = x_line_data[40:44]
        #print("ARP:", arp_type_code)
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
            src_port = x_line_data[68:72]
            dst_port = x_line_data[72:76]

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

            elif l3_pid == '06': #TCP l3 pid
                #http (port 80 = 0050) and tls (port 443 == 01bb)
                if src_port == "0050" or dst_port == "0050":
                    packet = "IPv4 TCP HTTP"
                    traffic_class_int = 5
                    #increase http counters when implemented
                    http_ctr += 1
                elif src_port == "01bb" or dst_port == "01bb":
                    packet = "IPv4 TCP TLS"
                    traffic_class_int = 4
                    tls_ctr += 1
                    #increase tls counters when implemented

            elif l3_pid == '11': #UDP l3 pid
                #dns (port 53 = 0035) and quic (ports 80 == 0050 and 443 == 01bb)
                if src_port == "0035" or dst_port == "0035":
                    packet = "IPv4 UDP DNS"
                    traffic_class_int = 6
                    dns_ctr += 1
                    #increase dns counter once implemented
                elif src_port == "0050" or src_port == "01bb" or dst_port == "0050" or dst_port == "01bb":
                    packet = "IPv4 UDP QUIC"
                    traffic_class_int = 7
                    quic_ctr += 1
                    #increase quic counter once implemented

    return packet, traffic_class_int, arp_request_ctr, arp_reply_ctr, icmp_request_ctr, icmp_reply_ctr, http_ctr, tls_ctr, dns_ctr, quic_ctr #return additional counters when implemented
