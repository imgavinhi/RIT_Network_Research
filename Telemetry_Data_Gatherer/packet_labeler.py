'''
This file will provide labels based on the l2_type of the ipv4 packet
'''

#this function defines labels for IPv4 packets. So far it only does ICMP Echo Requests and Echo Replies
#utilizes traffic class ints of 3 and 4
def ipv4_types(x_line_data, icmp_request_ctr, icmp_reply_ctr):
    traffic_class_int = 0
    packet = "No Match"
    l3_pid = x_line_data[46:48]

    #01 for ICMP, 11 for UDP, 06 for TCP, 02 for IGMP

    if l3_pid == '01':
        icmp_type_code = x_line_data[68:70] #was 68:72 to get icmp type and code
        #print(icmp_type_code)
        #input("stop to debug")
        
        #request type/code = 0800
        #reply type/code = 0000
        if icmp_type_code == '08': #was 0800
            packet = 'IPv4 ICMP Request'
            traffic_class_int = 3
            icmp_request_ctr = icmp_request_ctr+1
        elif icmp_type_code == '00': #was #0000
            packet = 'IPv4 ICMP Reply'
            traffic_class_int = 4
            icmp_reply_ctr = icmp_reply_ctr+1

            print("Req: ", icmp_request_ctr, " Rep: ", icmp_reply_ctr)

    return packet, traffic_class_int, icmp_request_ctr, icmp_reply_ctr

#this function defines labels for ARP packets
#utilizes traffic class ints of 1 and 2
def arp_labeler(x_line_data, arp_request_ctr, arp_reply_ctr):
    traffic_class_int = 0
    packet = "No Match"
    l2_type = x_line_data[24:28]
    if l2_type == "0806":
        arp_type_code = x_line_data[40:44] #double check when running
        #print("ARP:", arp_type_code)
        if arp_type_code == "0001":
            packet = "ARP Echo Request"
            traffic_class_int = 1
            arp_request_ctr = arp_request_ctr + 1
        elif arp_type_code == "0002":
            packet = "ARP Echo Reply"
            traffic_class_int = 2
            arp_reply_ctr = arp_reply_ctr + 1
    return packet, traffic_class_int, arp_request_ctr, arp_reply_ctr

