import csv

def read_lookup_table(file_path):
    lookup = {}
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip the table header row
        csv_reader = list(csv_reader)
        for row in csv_reader:
            if len(row) < 3: continue # skip in case of not enough data
            dstport, protocol, tag = row
            lookup[(int(dstport), protocol.lower())] = tag.lower()

    # print(lookup) # (25, 'tcp'): 'sv_p1', (68, 'udp'): 'sv_p2'
    return lookup

def parse_flow_log_line(line):
    # split long flow log string into 14 parts
    # version, account_id, interface_id, src_add, dst_add, srcport, dstport, protocol, packets, bytes, start, end, action, status
    parts = line.split()
    # invalid line, return none
    if len(parts) < 14:
        return None

    # grabbing destination port (index 6) and protocol (index 7)
    dstport = int(parts[6])

    # map protocol num to str
    protocol = {6: 'tcp', 17: 'udp', 1: 'icmp'}.get(int(parts[7]), 'unknown')
    return dstport, protocol

def process_flow_log(log_file_path, lookup_table):
    tag_counts = {}
    port_protocol_counts = {}

    # open flow_log.txt, parse and check counts
    with open(log_file_path, 'r') as file:
        for line in file:
            # function to parse protocols
            parsed = parse_flow_log_line(line)
            if parsed:
                dstport, protocol = parsed

                # count port/protocol combinations
                key = (dstport, protocol)
                port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1

                # assign and count tags
                # search in lookup_table, default untagged
                tag = lookup_table.get(key, 'Untagged')
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print("tag_counts: ", tag_counts)
    print("port_protocol_counts: " , port_protocol_counts)
    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    # open output.txt file and write results to it
    with open(output_file, 'w') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            # print(f"{tag},{count}\n")
            file.write(f"{tag},{count}\n")

        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            # print(f"{port},{protocol},{count}\n")
            file.write(f"{port},{protocol},{count}\n")

def main():
    # function to get lookup table from csv
    print("reading look up table")
    lookup_table = read_lookup_table('lookup_table.csv')

    print("look up table:")
    for key, value in lookup_table.items():
        print(f"{key}: {value}")

    # function to parse each line in flow_log.txt to tag counts and port protocol counts
    tag_counts, port_protocol_counts = process_flow_log('flow_log.txt', lookup_table)

    # write result to output.txt with hashmaps
    write_output(tag_counts, port_protocol_counts, 'output.txt')
    print("results written to output.txt")

# Test the function
if __name__ == "__main__":
    # test lookups
    # test_cases = [
    #     (25, 'tcp'),
    #     (443, 'tcp'),
    #     (68, 'udp'),
    #     (110, 'tcp'),
    #     (8080, 'tcp') # not in lookup table
    # ]

    # print("\nTesting specific lookups:")
    # for port, protocol in test_cases:
    #     tag = lookup_table.get((port, protocol), "Untagged")
    #     print(f"Port: {port}, Protocol: {protocol} -> Tag: {tag}")


    main()

    # sample flow log entry
    # 2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK

    # version -> 2
    # account id -> 123456789012
    # interface id -> eni-0a1b2c3d
    # source address -> 10.0.1.201
    # destination address -> 198.51.100.2
    # source port -> 443
    # destination port -> 49153
    # protocol -> 6 (tcp)
    # packets -> 25
    # bytes -> 20000
    # start time -> 1620140761
    # end time -> 1620140821
    # action -> ACCEPT
    # log status -> OK

    # items we grab - destination port, protocol, tag