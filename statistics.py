# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information

class Stats():
    def __init__(self):
        pass

    def data_collector(self,addr,qlist,rlist,qrlist):
        qsent=0
        qrecv=0
        rsent=0
        rrecv=0
        val=0
        c=0
        avgRtt=0
        #print addr

        for i,line in enumerate(qlist):
            if line.src_addr[0] == addr:
                qsent=qsent+1
            if line.dst_addr[0] == addr:
                qrecv=qrecv+1
        for j,line in enumerate(rlist):
            if line.src_addr[0]== addr:
                rsent = rsent+1
            if line.dst_addr[0]== addr:
                rrecv = rrecv+1
        for line in qrlist:
            if not line[0]=='bogus' and not line[1]=='bogus':
                if line[0].src_addr[0] == addr:
                    val =val+line[2]
                    c=c+1
        avgRtt=val/c
        return qsent,qrecv,rsent,rrecv,avgRtt
