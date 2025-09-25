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
    http_counter = 0
    tls_counter = 0
    dns_counter = 0
    quic_counter = 0

    no_match_counter = 0

    prediction_counter_list = []

    for i in predictions:
        if i == 0:
            #arp req
            packet_type = "ARP Request"
            arp_req_counter += 1
        elif i == 1:
            #arp rep
            packet_type = "ARP Reply"
            arp_rep_counter += 1
        elif i == 2:
            #icmp req
            packet_type = "ICMP Request"
            icmp_req_counter += 1
            ipv4_counter += 1
        elif i == 3:
            #icmp rep
            packet_type = "ICMP Reply"
            icmp_rep_counter += 1
            ipv4_counter += 1
        else:
            packet_type = "No Match"
            no_match_counter += 1

        ts_list.append(packet_type)

        packet_counter += 1
        packet_class = []
        packet_type = ""
    
    print("Total Packets:\t", packet_counter)
    print("IPv4 Packets:\t", ipv4_counter)
    print("#-Other:\t", no_match_counter)
    print("0-ARP Request:\t", arp_req_counter)
    print("1-ARP Reply:\t", arp_rep_counter)
    print("2-ICMP Request:\t", icmp_req_counter)
    print("3-ICMP Reply:\t", icmp_rep_counter)
    print("HTTP:\t", http_counter)
    print("TLS:\t", tls_counter)
    print("DNS:\t", dns_counter)
    print("QUIC:\t", quic_counter)
