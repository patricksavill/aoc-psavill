# First three bits are the version
# Next three bits are type ID
# These are both binary numbers

# Then, dependent upon the type ID:
# ID 4 - Literal value
#   four bits for each with a leading bit (so 5 total)
#   leading 0 means it's the last packet, 1 means not
#   At the end add together the binary and convert
#   so 3 packets would be a 12 bit number

# ID !-4 (anything else) is an OPERATOR:
#  Length ID: 0 = 15 bits next are total length
#    in bits of the rest of the subpackets
#  Length ID: 1 = 11 bits next are total
#    number of subpackets to come

total = 0

def process_packet(candidate, c_index):
    # First three are version

    # Test for leading zeros
    while candidate[c_index:c_index + 4] == "0000":
        print("Cruft")
        c_index += 4

    version_id = candidate[c_index:c_index + 3]
    print("Version: " + str(int(version_id, 2)))
    c_index += 3
    type_id = candidate[c_index:c_index + 3]
    c_index += 3

    if (type_id == "100"):
        # Getting a value
        #   four bits for each with a leading bit (so 5 total)
        #   leading 0 means it's the last packet, 1 means not
        end_value = False
        while not end_value:
            value_portion = candidate[c_index:c_index + 5]
            # print(value_portion)
            c_index += 5
            if value_portion[0] == "0":
                # This is the final packet
                end_value = True
    else:
        # Getting an operator
        if(c_index > len(candidate)):
            return c_index
        length_id = candidate[c_index]
        c_index += 1
        if length_id == "0":
            # Next 15 bits are a number
            length_bits = candidate[c_index:c_index + 15]
            c_index += 15
            decimal_length = int(length_bits, 2)
            # print(decimal_length)

            # TODO process this subpacket
            print("Should process")
            subpacket = candidate[c_index:c_index + decimal_length]
            c_index = process_packet(candidate, c_index)
            # c_index += decimal_length
        else:
            # Next 11 bits are a number
            length_packets = candidate[c_index:c_index + 11]
            c_index += 11
            decimal_packets = int(length_packets, 2)
            print(decimal_packets)
            # TODO process this subpacket
            print("Should process")
            subpackets = candidate[c_index:(c_index + decimal_packets * 11)]
            c_index = process_packet(candidate, c_index)
            # c_index += decimal_packets * 11
            wip = 0

    # Due to hexadecimal notation we should always
    # end processing with an index as a multiple of 4
    if c_index % 4 != 0:
        c_index += (4 - c_index % 4)

    # We now test if the next 4 bits are all zeros
    # If they are, they are cruft from hex encoding
    if candidate[c_index:c_index + 4] == "0000":
        print("Cruft")
        c_index += 4
    return c_index


decoder_map = {"0": "0000", "1": "0001", "2": "0010",
               "3": "0011", "4": "0100", "5": "0101",
               "6": "0110", "7": "0111", "8": "1000",
               "9": "1001", "A": "1010", "B": "1011",
               "C": "1100", "D": "1101", "E": "1110",
               "F": "1111"}

all_lines = []
with open("day16.txt") as file:
    all_lines = file.readlines()

master_packet = ""
for char in all_lines[0].rstrip("\n"):
    master_packet += decoder_map[char]

print(master_packet)
index = 0

process_packet(master_packet, 0)

exit(0)
# while index < len(master_packet):
#     # First three are version
#     version_id = master_packet[index:index + 3]
#     print("Version: " + str(int(version_id, 2)))
#     index += 3
#     type_id = master_packet[index:index + 3]
#     index += 3
#
#     if (type_id == "100"):
#         # Getting a value
#         #   four bits for each with a leading bit (so 5 total)
#         #   leading 0 means it's the last packet, 1 means not
#         end_value = False
#         while not end_value:
#             value_portion = master_packet[index:index + 5]
#             # print(value_portion)
#             index += 5
#             if value_portion[0] == "0":
#                 # This is the final packet
#                 end_value = True
#     else:
#         # Getting an operator
#         length_id = master_packet[index]
#         index += 1
#         if length_id == "0":
#             # Next 15 bits are a number
#             length_bits = master_packet[index:index + 15]
#             index += 15
#             decimal_length = int(length_bits, 2)
#             # print(decimal_length)
#
#             # TODO process this subpacket
#             print("Should process")
#             subpacket = master_packet[index:index + decimal_length]
#             process_packet(subpacket)
#             index += decimal_length
#         else:
#             # Next 11 bits are a number
#             length_packets = master_packet[index:index + 11]
#             index += 11
#             decimal_packets = int(length_packets, 2)
#             print(decimal_packets)
#             # TODO process this subpacket
#             print("Should process")
#             for i in range(decimal_packets):
#                 subpacket = master_packet[index:(index + 11)]
#                 process_packet(subpacket)
#                 index += 11
#             wip = 0
#
#     # Due to hexadecimal notation we should always
#     # end processing with an index as a multiple of 4
#     if index % 4 != 0:
#         index += (4 - index % 4)
#
#     # We now test if the next 4 bits are all zeros
#     # If they are, they are cruft from hex encoding
#     if master_packet[index:index + 4] == "0000":
#         print("Cruft")
#         index += 4
