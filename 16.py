from operator import mul
from functools import reduce

def bits_to_int(bits):
    return int(bits, 2)

def hex_to_bits(hex_str):
    bits =  bin(int(hex_str, 16))[2:]
    padding = len(hex_str)*4 - len(bits)
    return '0'*padding + bits


def read_n_bits_int(n):
    def fn(bitstring):
        bits = bitstring[:n]
        return bits_to_int(bits), bitstring[n:]

    return fn


read_single = read_n_bits_int(1)
read_triple = read_n_bits_int(3)
read_quadruple = read_n_bits_int(4)

read_version = read_triple
read_type_id = read_triple
read_length_type_id = read_single

read_literal_segment = read_quadruple

read_subpackets_length = read_n_bits_int(15)
read_subpackets_number = read_n_bits_int(11)


literal_type_id = 4
is_literal = lambda type_id: type_id == literal_type_id


def literal_segments_to_int(segment_ints):
    multiplier = 1
    total = 0

    for i in segment_ints[::-1]:
        total += i*multiplier
        multiplier *= 16

    return total

def read_literal(bitstring):
    segment_ints = []

    cont = True
    while cont:
        cont = int(bitstring[0])
        segment_int, bitstring = read_literal_segment(bitstring[1:])
        segment_ints.append(segment_int)

    return literal_segments_to_int(segment_ints), bitstring

# For part 2
operators = {0: sum,
             1: lambda values: reduce(mul, values),
             2: min,
             3: max,
             5: lambda packets: 1 if packets[0] > packets[1] else 0,
             6: lambda packets: 1 if packets[0] < packets[1] else 0,
             7: lambda packets: 1 if packets[0] == packets[1] else 0}

def read_packet(bitstring):
    version, bitstring = read_version(bitstring)
    type_id, bitstring = read_type_id(bitstring)
    is_literal = type_id == literal_type_id

    if is_literal:
        body, bitstring = read_literal(bitstring)
    else:
        # we do a little mutual recursion
        length_type_id, bitstring = read_length_type_id(bitstring)

        read_by_length_fns = (read_subpackets_length, read_subpackets_by_length)
        read_by_number_fns = (read_subpackets_number, read_subpackets_by_number)
        read_sp_fn, read_sp_by_fn = read_by_length_fns if length_type_id == 0 else read_by_number_fns
        n, bitstring = read_sp_fn(bitstring)
        body, bitstring = read_sp_by_fn(n, bitstring)

    return {'version': version,
            'type': 'literal' if is_literal else operators[type_id],
            'body': body}, \
            bitstring


def read_subpackets_by_length(length, bitstring):
    sub_bitstring = bitstring[:length]

    subpackets = []

    while sub_bitstring:
        subpacket, sub_bitstring = read_packet(sub_bitstring)
        subpackets.append(subpacket)

    return subpackets, bitstring[length:]

def read_subpackets_by_number(n, bitstring):
    subpackets = []

    for i in range(n):
        subpacket, bitstring = read_packet(bitstring)
        subpackets.append(subpacket)

    return subpackets, bitstring


## Part 1
def sum_versions(packet):
    total = 0

    total += packet['version']
    is_literal = packet['type'] == 'literal'

    if not is_literal:
        total += sum(map(sum_versions, packet['body']))

    return total

def sum_versions_hex(hex_str):
    bin_str = hex_to_bits(hex_str)
    packet, _ = read_packet(bin_str)
    return sum_versions(packet)


## Part 2
def evaluate_packet(packet):
    if packet['type'] == 'literal':
        return packet['body']

    op = packet['type']
    subpackets = packet['body']
    subpacket_values = list(map(evaluate_packet, subpackets))

    return op(subpacket_values)


def evaluate_hex(hex_str):
    bin_str = hex_to_bits(hex_str)
    packet,_ = read_packet(bin_str)
    return evaluate_packet(packet)

