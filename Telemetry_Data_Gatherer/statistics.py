'''
generate summary statistics for parsed data packets
this includes number of different types of packets, etc
'''
import csv

def statistics(csv_file):
    packet_count = 0
    av_size = 0
    max_size = 0
    min_size = 0

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            #print(row)
            packet_count += 1
            leng = row[4]
            int_leng = int(leng, 16)
            
            min_size = int_leng
            av_size += int_leng
            max_size = max(max_size, int_leng)
            min_size = min(min_size, int_leng)

            if packet_count > 0:
                av_size /= packet_count
        
        print(packet_count)
        print(av_size)
        print(max_size)
        print(min_size)
                #packet_type = row[7] #PID vs EtherType?
