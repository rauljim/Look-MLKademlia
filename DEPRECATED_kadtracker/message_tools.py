# Copyright (C) 2009 Raul Jimenez
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information

import sys

import logging

import bencode
from identifier import Id, ID_SIZE_BYTES, IdError
from node import Node


logger = logging.getLogger('dht')



IP4_SIZE = 4 #bytes
IP6_SIZE = 16 #bytes
ADDR4_SIZE = IP4_SIZE + 2 # IPv4 address plus port
ADDR6_SIZE = IP6_SIZE + 2 # IPv6 address plus port
C_NODE_SIZE = ID_SIZE_BYTES + ADDR4_SIZE
C_NODE2_SIZE = ID_SIZE_BYTES + ADDR6_SIZE

IP6_PADDING = '\x00' * 10 + '\xff\xff'

class DecodingError(Exception):
    pass

class AddrError(Exception):
    pass

#class IP6Addr(AddrError):
#    pass
# TODO2: deal with IPv6 address (we ignore them now)


def bin_to_int(bin_str):
    return ord(bin_str[0]) * 256 + ord(bin_str[1])

def int_to_bin(i):
    return chr(i/256) + chr(i%256)

def bin_to_ip(bin_str):
    if len(bin_str) == IP4_SIZE:
        return '.'.join([str(ord(b)) for b in bin_str])
    if len(bin_str) != IP6_SIZE:
        raise DecodeError, 'compact_ip: invalid size (%d)' % len(bin_str)
    if not bin_str.startswith(IP6_PADDING):
        raise AddrError, 'IPv4 and v6 should not be mixed!'
    c_ip = bin_str[len(IP6_PADDING):]
    return '.'.join([`ord(byte)` for byte in c_ip])



def ip_to_bin(ip_str):
    return ''.join([chr(int(b)) for b in ip_str.split('.')])

def compact_addr(addr):
    return ''.join((ip_to_bin(addr[0]), int_to_bin(addr[1])))

def uncompact_addr(c_addr):
    if c_addr[-2:] == '\0\0':
        logger.warning('c_addr: %r > port is ZERO' % c_addr)
        raise AddrError
    return (bin_to_ip(c_addr[:-2]), bin_to_int(c_addr[-2:]))

def compact_peers(peers):
    return [compact_addr(peer) for peer in peers]

def uncompact_peers(c_peers):
    peers = []
    for c_peer in c_peers:
        try:
            peers.append(uncompact_addr(c_peer))
        except (AddrError):
            pass
    return peers

def compact_nodes(nodes):
    return ''.join([node.id.bin_id + compact_addr(node.addr) \
                    for node in nodes])
    
def uncompact_nodes(c_nodes):
    nodes = []
    if len(c_nodes) % C_NODE_SIZE != 0:
        return nodes
        raise DecodeError, 'invalid size (%d) %s' % (len(c_nodes),
                                                     c_nodes)
    
        
    for begin in xrange(0, len(c_nodes), C_NODE_SIZE):
        node_id = Id(c_nodes[begin:begin + ID_SIZE_BYTES])
        try:
            node_addr = uncompact_addr(
                c_nodes[begin+ID_SIZE_BYTES:begin+C_NODE_SIZE])
        except AddrError:
            pass
        else:
            node = Node(node_addr, node_id)
            nodes.append(node)
    return nodes

def compact_nodes2(nodes):
    return [node.id.bin_id + IP6_PADDING + compact_addr(node.addr) \
            for node in nodes]
    
def uncompact_nodes2(c_nodes):
    nodes = []
    for c_node in c_nodes:
        node_id = Id(c_node[:ID_SIZE_BYTES])
        try:
            node_addr = uncompact_addr(c_node[ID_SIZE_BYTES:]) 
        except (AddrError):
            logger.warning('IPv6 addr in nodes2: %s' % c_node)
        else:
            node = Node(node_addr, node_id)
            nodes.append(node)
    return nodes


