# Illumio Tech Assessment

Language choice: python3

## Brief Walkthrough

I had to do some quick studying to see what a [flow log](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields) was and how to work with it, and then I made a .txt file with the example flow logs and a .csv file with the example lookup table.

The .py program has a few functions. First, it grabs the lookup table and stores the destination port and protocol as keys, with the tag as its value in a hashmap.

```python3
(25, 'tcp'): sv_p1
(68, 'udp'): sv_p2
(23, 'tcp'): sv_p1
```

Then it takes that lookup table and opens up the flow_log.txt file. After parsing each row of that file for their destination port and protocol, it keeps a count of the port/protocol using a hashmap and checks the lookup table for tag count as well.

```python3
tag_counts:  {'Untagged': 8, 'sv_p2': 2, 'sv_p1': 2, 'email': 3, 'sv_p5': 1}

port_protocol_counts:  {(49153, 'tcp'): 1, (49154, 'tcp'): 1, (49155, 'tcp'): 1, (49156, 'tcp'): 1, (49157, 'tcp'): 1, (49158, 'tcp'): 1, (80, 'tcp'): 1, (1024, 'tcp'): 1, (443, 'tcp'): 1, (23, 'tcp'): 1, (25, 'tcp'): 1, (110, 'tcp'): 1, (993, 'tcp'): 1, (143, 'tcp'): 1, (68, 'udp'): 1, (0, 'icmp'): 1}
```

Finally, there is a function that writes the results to an output.txt file, using the previously found counts.

## How to Run

1. Ensure python3 is installed on the system
2. To copy the repository, click the green code button and either copy the URL or download the repository's files
   - if using the URL, go to the folder where you would like these files to be downloaded
   - run this command `git clone [URL_copied_from_Github]` and it will download the files from git
3. Open the folder you've downloaded the repository to
4. Ensure flow_log.txt and lookup_table.csv are in the same directory as the python script
5. Run the python script using `python3 flow_log_parser.py`
6. Check the output.txt file that will be generated in the same directory, which will contain the tag counts and port/protocol combination counts

## Assumptions

The program works assuming flow logs are:

- formatted as default logs
- version number 2

and looks like:

```
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
```

- version, account id, interface id, source address, destination address,
- source port, destination port, protocol, packets, bytes,
- start time, end time, action, status

If a flow log does not have these 14 parts seperated by a space in its string, it will skip it. Currently the program does not check for the validity of its parts, such as searching for an existing account id or valid times, it is assumed these are valid fields.

The lookup table is expected to look like:

```csv
dstport,protocol,tag
25,tcp,sv_P1
68,udp,sv_P2
23,tcp,sv_P1
```

With only 3 columns, and the header in the order of dstport, protocol and then tag.

Assuming the flow logs and the lookup table are in this format, the program can write the correct counts to the output.txt file correctly.

### Extra

- [Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) to keyword (tcp, icmp, udp, etc.)
