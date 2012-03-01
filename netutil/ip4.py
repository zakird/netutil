import socket
import struct
import re

FULL_MASK = int("0xffffffff", 16)
IP_REGEX = re.compile('(\d{1,3}\.){3}\d{1,3}')

def str_to_int(ip):
    "returns integer version of IP address string (e.g. 1.2.3.4)"
    return struct.unpack('!L', socket.inet_aton(ip))[0]

def int_to_str(n):
    "returns string version (e.g. 1.2.3.4) from integer version"
    return socket.inet_ntoa(struct.pack('!L', n))

def make_mask(n):
    return (2L << int(n) - 1) - 1

def make_inverted_mask(n):
    return int(FULL_MASK) >> int(n)

def get_bounds_from_cidr(n):
    "returns lowest and highest IP address for a given IP block in CIDR notation (128.255.0.0/24"
    lower_bound, prefix_length = n.split("/")
    lower_bound_i = str_to_int(lower_bound)
    upper_bound = lower_bound_i | make_inverted_mask(make_mask(prefix_length))
    return (lower_bound_i, upper_bound)
