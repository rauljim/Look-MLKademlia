# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information
import decimal
import pymdht.core.identifier as identifier

class Plot():

   def __init__(self):
        pass

   def cdf(self,results):
       num_results = len(results)
		#print num_results
       results.sort()
       try:
           step = 1. / num_results
       except(ZeroDivisionError):
           print 'No data'
       cum = []
       values = []
       for i, v in enumerate(results):
           cum.append((i+1) * step)
           values.append(v)
       return cum, values


   def get_rtt_data(self,list,source,type,infoh):
       counter=0
       dlist=[]
       data=[]
       mylist=list
      
       if source:
          for item in mylist:
             if item[0].src_addr[0]== source and not item[1]=='bogus':
                if type == 'All':
                   rtt=self.get_rtt(item)
                   data.append(rtt)
                elif item[0].query_type==type:
                    if item[0].query_type == 'get_peers':
                        if infoh:
                            if repr(item[0].infohash)==infoh:
                               rtt=self.get_rtt(item)
                               data.append(rtt)
                        else:
                           rtt=self.get_rtt(item)
                           data.append(rtt)
                    else:
                       rtt=self.get_rtt(item)
                       data.append(rtt)
                  
       return data

   def get_rtt(self,item):
      
          d=str(item[2])
          rtt=0
          if not( d== '0') :
             #counter=counter+1
             #dlist.append(d)
             decimal.getcontext().prec = 4
             rtt=round(float(d),4)
          return rtt
     

   def timestamps(self,list,source,infoh,type):
       qts=[]
       rts=[]
       c=0
       mylist=list
       
       		
      # 
       if source:
           for item in mylist:
                if item[0].src_addr[0]== source:
                   if type == 'All':
                 
                      c=c+1
                      q,r=self.find_qts_rts(c,item)
                      qts.append(q)
                      rts.append(r)
                   elif item[0].query_type == type:

                      if item[0].query_type == 'get_peers':
                         if infoh:
                            if repr(item[0].infohash)==infoh:
                               c=c+1
                               q,r=self.find_qts_rts(c,item)
                               qts.append(q)
                               rts.append(r)
                         else:
                            c=c+1
                            q,r=self.find_qts_rts(c,item)
                            qts.append(q)
                            rts.append(r)
                      else:
                         c=c+1
                         q,r=self.find_qts_rts(c,item)
                         qts.append(q)
                         rts.append(r)
       return qts,rts

   def find_qts_rts(self,c,item):
       #c=c+1
       q=''
       r=''
       q=(c,round(float(item[0].ts),4))
       if not item[1]=='bogus':
           r=(c,round(float(item[1].ts),
                               4))
       else:
           r=(c,0)
       return q,r

   def convergence(self,list,source,infoh):
       dist=[]
       c=0
       mylist=list
       if not infoh or not source:
           assert 0
       for item in mylist:
           if (item[0].query_type == 
               'get_peers')and (item[0].src_addr[0]== 
                                source)and (repr(item[0].infohash)
                                            ==infoh):
               
               if not item[1]=='bogus':
                   
                   if item[1].dist_from_sender:
						#print item[1].dist_from_sender
                       c=c+1
							#c=c+1
                       dist.append((item[0].ts,item[1].
                                    dist_from_sender))
					
					
       return dist

   def get_traffic_data(self,list,source):
       gpcount=0
       fncount=0
       pcount=0
       apcount=0
       mylist=list

	
       for item in mylist:
           if item[0].src_addr[0]== source: 
               
				#d=(counter,self.list[i][2])
               if item[0].query_type=='get_peers':
                   gpcount=gpcount+1
               elif item[0].query_type=='find_node':
                   fncount=fncount+1
               elif item[0].query_type=='ping':
                   pcount=pcount+1
               elif item[0].query_type=='announce_peer':
                   apcount=apcount+1

       return gpcount,fncount,pcount,apcount
