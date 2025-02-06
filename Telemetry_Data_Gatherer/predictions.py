def packet_choice(predictions):
    ts_list = [] #for troubleshooting

    packet_class = []
    packet_type = "No Match"
    packet_counter = 0
    prediction_col = 0

    arp_req_counter = 0
    arp_rep_counter = 0
    ipv4_counter = 0
    icmp_req_counter = 0
    icmp_rep_counter = 0

    no_match_counter = 0

    prediction_counter_list = []

    for i in predictions:
       #print(i)
        if i == 1:
            #arp req
            packet_type = "ARP Request"
            arp_req_counter += 1

        elif i == 2:
            #arp rep
            packet_type = "ARP Reply"
            arp_rep_counter += 1

        elif i == 3:
            #icmp req
            packet_type = "ICMP Request"
            icmp_req_counter += 1
            ipv4_counter += 1

        elif i == 4:
            #icmp rep
            packet_type = "ICMP Reply"
            icmp_rep_counter += 1
            ipv4_counter += 1
        
        else:
            packet_type = "Other"
            no_match_counter += 1

        #for debugging:
        ts_list.append(packet_type)

        packet_counter += 1
        packet_class = []
        packet_type = ""
    
    print("\nPrediction values:\n", predictions[:20])

    print("\nPacket_type list:\n", ts_list[:20])

    print("Total Packets:\t", packet_counter)
    print("IPv4 Packets:\t", ipv4_counter)
    print("0-Other:\t", no_match_counter)
    print("1-ARP Request:\t", arp_req_counter)
    print("2-ARP Reply:\t", arp_rep_counter)
    print("3-ICMP Request:\t", icmp_req_counter)
    print("4-ICMP Reply:\t", icmp_rep_counter)
