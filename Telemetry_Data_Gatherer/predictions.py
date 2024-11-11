def packet_choice(predictions):
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
        if i == 1:
            #arp req
            packet_type = "ARP"
            arp_req_counter += 1

        elif i == 2:
            #arp rep
            packet_type = "ARP"
            arp_rep_counter += 1

        elif i == 3:
            #icmp req
            packet_type = "ICMP"
            icmp_req_counter += 1
            ipv4_counter += 1

        elif i == 4:
            #icmp rep
            packet_type = "ICMP"
            icmp_rep_counter += 1
            ipv4_counter += 1
        
        else:
            packet_type = "Other"
            no_match_counter += 1

        packet_counter += 1
        packet_class = []
        packet_type = ""

    print("Total Packets:\t", packet_counter)
    print("IPv4 Packets:\t", ipv4_counter)
    print("0-Other:\t", no_match_counter)
    print("1-ARP Request:\t", arp_req_counter)
    print("2-ARP Reply:\t", arp_rep_counter)
    print("3-ICMP Request:\t", icmp_req_counter)
    print("4-ICMP Reply:\t", icmp_rep_counter)
