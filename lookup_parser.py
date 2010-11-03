import sys
from socket import inet_ntoa

import pcap
import dpkt
import pcapy
import pymdht.core.message as message


if len(sys.argv) == 4:
    # Read from file
    pcap = pcap.pcap(sys.argv[3])#
elif len(sys.argv) == 3:
    # Live capture (not tested)
    pcap = pcap.pcap('any')
else:
    print 'usage: lookup_parser my_ip my_port [pcpcapap_file]'
    sys.exit(1)
    
# Our client is working on UDP port
my_addr = (sys.argv[1], int(sys.argv[2]))

start_ts = None
start_query = None
num_queries = 0
num_responses = 0
counter=0
c=0
#cap = pcapy.open_live('any', 100, 1, 0)
#f=open('log11.pcap')
#pcap=dpkt.pcap.Reader(f)
#(header, payload) = cap.next()
for (ts, raw_packet) in pcap:
    
    ip_packet = dpkt.ethernet.Ethernet(raw_packet).ip
    #print 'hi packet',repr(ip_packet.src)
    src_addr = (inet_ntoa(ip_packet.src), ip_packet.udp.sport)
    dst_addr = (inet_ntoa(ip_packet.dst), ip_packet.udp.dport)
    try:
        msg = message.IncomingMsg(ip_packet.data.data, src_addr, True)
        counter=counter+1
    except(message.MsgError):
        print message.MsgError
        c=c+1
        #print 'ERROR:', ip_packet.data.data
        continue
    if src_addr == my_addr:
        if msg.type == message.QUERY and msg.query == message.GET_PEERS:
            num_queries += 1
            if not start_query:
                start_ts = ts
                start_query = msg
                print 'LOOKUP: %r log_distance: %d' % (
                    msg.info_hash,
                    msg.info_hash.log_distance(msg.sender_id))
            print '%.3f QUERY(TID: %d) to %r' % (
                ts - start_ts,
                ord(msg.tid[0]),
                dst_addr)
                
    elif dst_addr == my_addr:
        if msg.type == message.RESPONSE and getattr(msg, 'token', None):
            num_responses += 1
            #print '%.3f RESPONSE(TID: %d) from %r(dist: %d)' % (
            #    ts - start_ts,
            #    ord(msg.tid[0]),
            #    src_addr,
            #    start_query.info_hash.log_distance(msg.sender_id))
            try:
                peers = msg.peers
                print '\t\t\t\t\t>>>>>>>>>> %d PEERS >>>>>>>>>>>>>' % (
                    len(msg.peers))
            except (AttributeError):
                pass
            try:
                for node in msg.nodes:
                    print '\t%r(dist: %d)' % (
                        node.addr,
                        node.id.log_distance(start_query.info_hash))
            except (AttributeError):
                pass
            try:
                for node in msg.nodes2:
                    print '\t2%r(dist: %d)' % (
                        node.addr,
                        node.id.log_distance(start_query.info_hash))
            except (AttributeError):
                pass
                
    else:
        print 'ERROR: src_addr: %r, dst_addr: %r' % (src_addr, dst_addr)
        continue
               
#print '%r'%msg.sender_id
#print 'num queries: %d, num responses: %d' % (num_queries, num_responses)
#print counter
#print c
        
        

