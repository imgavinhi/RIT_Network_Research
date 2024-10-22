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
        
    print("Definitions: ")
    print("|Correlation|\nA statistical measurement that shows the extent that two variables are linearly related. This means that the two variables change together at a constant rate. It’s a tool used for describing simple relationships without making a statement about causes and effects.\n|Correlation Coefficient|\n Correlation coefficient is a number between –1 and+1 calculated to represent the linear relationship of two variables. Negative one represents a perfect negative correlation, meaning when one variable increases the other decreases proportionally. Positive 1 indicates that two variables have a perfect positive correlation, meaning when one increases the other increases proportionally.\n|Correlation Metrics|\nCorrelation metrics measure whether or not there is a relationship between two variables. Some common ones include correlation coefficients, matrices, and covariance.\n|Correlation Matrix|\nA correlation matrix is a table that shows the correlation coefficients between a set of variables. A correlation matrix can be used to identify patterns and trends in data as well as to understand the relationships between multiple variables.")

    print("Count: " + str(packet_count))
    print("Average Packet Length: " + str(av_size))
    print("Maximum Packet Length: " + str(max_size))
    print("Minimum Packet Length: " + str(min_size))
                #packet_type = row[7] #PID vs EtherType?
