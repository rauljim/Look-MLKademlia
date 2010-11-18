# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information

#Testing git

import wx
import operator
import os
import sys
import binascii
import decimal
import lookupconverge as lcv
from socket import inet_ntoa
import pcap
import dpkt
import pymdht.core.message as message
import pymdht.core.message_tools as mt
import pymdht.core.identifier as identifier
import pymdht.core.logging_conf as logging_conf

import filterscreen as fsc
#import filters
import mainclass
import graphgui
import statgui


#logging_conf.setup()


class Gui(wx.Frame):
    
    list=[]
    QueResErrList=[]
    querieslist=[]
    responseslist=[]
    errorslist=[]
    filename=''
    infohash=''
    srcaddr=''
    infohashlist=[]
    src=''
    dst=''
    qlist=[]
    rlist=[]
    f1=''
    f=''
    count=0
   # obj=qr.MatchQandR(filename)
    #objQ=q.QueriesBisector(filename)
    #objR=r.ResponseBisector(filename)
    

    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle,
            size=(1000,800))
        #self.m=map.Mappings()
        #a=self.obj.match_all_qr()
        #self.list=self.a
        self.toolbar=''
        self.createmenu()
        self.createToolBar()
        self.createcontrols()
        #self.loadList1()
        #self.loadList2()
        self.bindings()
        self.src=''
        self.dst=''
        self.col1toggled=False
        self.col2toggled=False
        self.col6toggled=False
        self.col3toggled=False
        self.ip_alias, self.id_alias, self.trans_alias = False,False,False

    def bindings(self):

        self.Bind(wx.EVT_BUTTON, self.filter, id=3)#filter button
        self.Bind(wx.EVT_BUTTON, self.no_filter, id=4)#no filter button
        self.Bind(wx.EVT_BUTTON, self.make_filter_expression, id=5)
        
        
        self.Bind(wx.EVT_TOOL, self.open_file, id=1)
        self.Bind(wx.EVT_TOOL, self.start_capture, id=2)
        self.Bind(wx.EVT_TOOL, self.quit, id=3)
        self.Bind(wx.EVT_TOOL, self.lookup_view_window, id=4)
        self.Bind(wx.EVT_TOOL, self.make_filter_expression, id=5)
        self.Bind(wx.EVT_TOOL, self.get_statistics, id=6)
        self.Bind(wx.EVT_TOOL, self.create_graph, id=7)
        self.Bind(wx.EVT_TOOL, self.get_help, id=8)


        self.Bind(wx.EVT_MENU, self.start_capture, id=109)
        self.Bind(wx.EVT_MENU, self.stop_capture, id=110)
   
        self.Bind(wx.EVT_MENU, self.match_all_qr, id=118)
        self.Bind(wx.EVT_MENU, self.match_get_peers_qr, id=119)
        self.Bind(wx.EVT_MENU, self.match_find_node_qr, id=120)
        self.Bind(wx.EVT_MENU, self.match_announce_peer_qr, id=121)
        self.Bind(wx.EVT_MENU, self.match_ping_qr, id=122)
        self.Bind(wx.EVT_MENU, self.query_with_no_response, id=130)
        #self.Bind(wx.EVT_MENU, self.response_with_no_query, id=131)

        self.Bind(wx.EVT_MENU, self.lookup_view_window, id=124)
        
        self.Bind(wx.EVT_MENU,self.make_filter_expression,id=123)

        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelect)
        self.lc.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.get_statistics)
        self.lc.Bind(wx.EVT_LIST_COL_CLICK, self.onListColClick)

        self.Bind(wx.EVT_MENU, self.open_file, id=101)

        self.ip.Bind(wx.EVT_LEFT_UP, self.onClick)

        self.id.Bind(wx.EVT_LEFT_UP, self.onClick) 
        self.tid.Bind(wx.EVT_LEFT_UP, self.onClick) 
        self.error.Bind(wx.EVT_LEFT_UP, self.onClick)
        self.nores.Bind(wx.EVT_LEFT_UP, self.onClick)


    def open_file(self,event):
        dlg = wx.FileDialog(self, "Choose a file", 
                                os.getcwd(), "", "*.*",
                                wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.filename = path#os.path.basename(path)
            self.SetStatusText(self.filename)
        dlg.Destroy()
        #objQ=q.QueriesBisector(self.filename)
        #self.infohashlist=objQ.find_infohash_from_file()
        #todo: check for file format here
        #print self.filename
        #objQ=q.QueriesBisector(self.filename)
        #objR=r.ResponseBisector(self.filename,self.infohash)
        
        obj=mainclass.MainClass()
        q,r,e,qre=obj.open_file(self.filename)
        #que=objQ.all_queries()
        #res=objR.all_response()
        #print len(q)
        self.querieslist=q
        self.responseslist=r

        self.errorslist=e
            #else:
               # print 'not found',item
        
        self.QueResErrList=qre
        #
#print(len(r))
        self.list=qre
        self.loadList1()
        
    def ip_id_trans_aliasing(self,id):
        result=[]
        obj=mainclass.MainClass()
   
        result=obj.check_aliasing(self.QueResErrList,id)
 
        return result

    def match_all_qr(self,event):
        self.list=self.QueResErrList

        self.loadList1()
        self.loadList2()

    def match_get_peers_qr(self,event):
        objqr=mainclass.MainClass()
        #a=objqr.match_get_peers_qr()
        a=objqr.get_peers_query_response(self.QueResErrList)
      
        self.list=a
  
        self.loadList1()

    def match_find_node_qr(self,event):
        objqr=mainclass.MainClass()
        #a=objqr.match_get_peers_qr()
        a=objqr.find_node_query_response(self.QueResErrList)
        self.list=a
        self.loadList1()

    def match_ping_qr(self,event):
        objqr=mainclass.MainClass()
        #a=objqr.match_get_peers_qr()
        a=objqr.ping_query_response(self.QueResErrList)
        self.list=a
        self.loadList1()

    def match_announce_peer_qr(self,event):
        objqr=mainclass.MainClass()
        #a=objqr.match_get_peers_qr()
        a=objqr.announce_peer_query_response(self.QueResErrList)
        self.list=a
        self.loadList1()

        
    def query_with_no_response(self,event):
        objqnr=mainclass.MainClass()
        a=objqnr.query_with_no_response(self.QueResErrList)
        self.list=a
        self.loadList1()

    def response_with_no_query(self,event):
        objrnq=mainclass.MainClass()
        a=objrnq.response_with_no_query(self.querieslist,
                                        self.responseslist,self.errorslist)
        self.list=a
        self.loadList1()



    def lookup_view_window(self,event):
 
        width = 1000
        height = 800
        obj=lcv.LookupConverge(None, mytitle,self.QueResErrList, 
                               (width, height)).Show()



    def no_filter(self,event):
        #obj=qr.Main()
        #a=obj.all_query_response_inline()
        self.list=self.QueResErrList

        self.loadList1()
        self.loadList2()

    def start_capture(self,event):
        #print 'hello'
        self.count=0
        self.f=open('myfile1.pcap','w')
        self.f1=dpkt.pcap.Writer(self.f)
        #ok=raw_input()
        pc = pcap.pcap('eth0')
        pc.setnonblock(True)


        pc.setfilter('udp dst port 6881')
       
        try:
            for ts,pkt in pc:
            
                self.f1.writepkt(pkt,ts)
        except KeyboardInterrupt:
            print '%s',sys.exc_type
            pc.close()
    def stop_capture(self,event):
        #print 'stop'
        self.count=1
        #pc.close()
        self.f.close()
        self.f1.close()

    def make_filter_expression(self,event):
         mytitle='Filter Screen Look@kad'
         width = 600
         heigh = 300
         objfsc=fsc.FilterScreen(self, mytitle,(width, height)).Show()

    
    def get_filter_values(self,values):
        self.filtertxt.Clear()
        self.filtertxt.WriteText(str(values))

    def filter(self,event):
        
        filtertext=self.filtertxt.GetValue()
        #filtered=filtertext.split()
        #self.filtertxt.SetValue(str(filtered))
        fobj=mainclass.MainClass()
        f= fobj.filter(self.QueResErrList,filtertext)
        #if f==True:
        #    filtered=filtertext.split()
        #    a=fobj.filter_data(self.filename,filtered)
        
        self.list = f
        self.loadList1()

    def get_statistics(self,event):
        width = 360
        height = 379
        #for i,line in enumerate(self.querieslist):
        #    print line.src_addr
        thisclick=event.GetEventObject()
        if thisclick == self.toolbar:
            self.srcaddr=''
 

        elif thisclick == self.lc:
            ix_selected = self.lc.GetNextItem(item=-1,
                                              geometry=wx.LIST_NEXT_ALL,
                                              state=wx.LIST_STATE_SELECTED)
            self.srcaddr=str(self.list[ix_selected][0].src_addr[0])
            
           
        obj=statgui.StatGui(None, 'Statistics',self.querieslist,
                            self.responseslist,self.QueResErrList,
                            self.srcaddr,
                            (width, height)).ShowModal()

    def create_graph(self,event):
        width = 2000
        height = 2000
        obj=graphgui.GraphGui(None, 'Graphs',self.QueResErrList, 
                        (width, height)).Show()

    def get_help(self,event):
        pass

    def quit(self,event):
        self.Destroy()





    def createcontrols(self):


        self.ip = wx.Panel(self, -1)
        self.id = wx.Panel(self, -1) 
        self.tid = wx.Panel(self, -1)
        self.nores = wx.Panel(self, -1)
        self.error = wx.Panel(self, -1)
        self.colorlbl=wx.StaticText(self,label="Color Indicators:")
        self.ipaliaslbl=wx.StaticText(self,label="IP Aliasing")

        self.idaliaslbl=wx.StaticText(self,label="ID Aliasing")
        self.tidlbl=wx.StaticText(self,label="Same TranactionIDs")
        self.noreslbl=wx.StaticText(self,label="No Response")
        self.errorlbl=wx.StaticText(self,label="Error")
        self.ip.SetBackgroundColour('plum')
        self.id.SetBackgroundColour('light green')
        self.tid.SetBackgroundColour('yellow')
        self.nores.SetBackgroundColour('light blue')
        self.error.SetBackgroundColour(wx.RED)

        self.filtertxt = wx.TextCtrl(self, size=wx.Size(400, -1))
        self.Filterbtn=wx.Button(self, 3, 'Filter', (50, 130))
        self.NoFilterbtn=wx.Button(self, 4, 'No Filter', (50, 130))
        self.Expressbtn=wx.Button(self, 5, 'Expression', (50, 130))
        self.nodelbl=wx.StaticText(self,label="Nodes/Log Distances")
        self.peerlbl=wx.StaticText(self,label="Peers")
        self.misclbl=wx.StaticText(self,label="Miscellaneous")
          # create and load the columns with header titles, set width
        self.lc = wx.ListCtrl(self, wx.ID_ANY,

             style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES)

        self.lc.InsertColumn(0,"No.")
        self.lc.SetColumnWidth(0, 50 )
        self.lc.InsertColumn(1,"QTime")
        self.lc.SetColumnWidth(1, 140)
        self.lc.InsertColumn(2,"RTime")
        self.lc.SetColumnWidth(2, 140)
        self.lc.InsertColumn(3,"RTT")
        self.lc.SetColumnWidth(3, 140)
        self.lc.InsertColumn(4,"Querier")
        self.lc.SetColumnWidth(4, 190)
        self.lc.InsertColumn(5,"Responder")
        self.lc.SetColumnWidth(5, 190)
        self.lc.InsertColumn(6,"Transaction Id")
        self.lc.SetColumnWidth(6, 130)
        
        self.lc2 = wx.ListCtrl(self, wx.ID_ANY,pos=(0,600),size=(950,50),
             style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES)
        self.lc2.InsertColumn(0,"Query/Response")
        self.lc2.SetColumnWidth(0, 150)  
        self.lc2.InsertColumn(1,"Querier Identifier / Distance")
        self.lc2.SetColumnWidth(1, 360)
        self.lc2.InsertColumn(2,"Responder Identifier / Distance")
        self.lc2.SetColumnWidth(2, 360)
        self.lc2.InsertColumn(3,"Version Q/R")
        self.lc2.SetColumnWidth(3, 100)
        

        self.nodestxt = wx.TextCtrl(self, wx.ID_ANY,
            value="",
            style=wx.TE_MULTILINE)

        self.peerstxt = wx.TextCtrl(self, wx.ID_ANY,
            value="",
            style=wx.TE_MULTILINE)

        self.misctxt = wx.TextCtrl(self, wx.ID_ANY,
            value="",
            style=wx.TE_MULTILINE)
    
        
        # use a vertical boxsizer as main layout sizer
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        # use a horizontal sizer for the buttons
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h1.Add(self.filtertxt,0)
        sizer_h1.Add(self.Filterbtn,0)
        sizer_h1.Add(self.Expressbtn,0)
        sizer_h1.Add(self.NoFilterbtn,0)
        sizer_h.Add(self.colorlbl,0)
        sizer_h.AddSpacer((20,0))
        sizer_h.Add(self.ipaliaslbl,0)
        sizer_h.AddSpacer((5,0))
        sizer_h.Add(self.ip,0)
        sizer_h.AddSpacer((20,0))
        sizer_h.Add(self.idaliaslbl,0)
        sizer_h.AddSpacer((5,0))
        sizer_h.Add(self.id,0)
        sizer_h.AddSpacer((20,0))
        sizer_h.Add(self.tidlbl,0)
        sizer_h.AddSpacer((5,0))
        sizer_h.Add(self.tid,0)
        sizer_h.AddSpacer((20,0))
        sizer_h.Add(self.noreslbl,0)
        sizer_h.AddSpacer((5,0))
        sizer_h.Add(self.nores,0)
        sizer_h.AddSpacer((20,0))
        sizer_h.Add(self.errorlbl,0)
        sizer_h.AddSpacer((5,0))
        sizer_h.Add(self.error,0)
        sizer_h2.Add(self.nodelbl,0)
        sizer_h2.AddSpacer((300,0))
        sizer_h2.Add(self.peerlbl,0)
        sizer_h2.AddSpacer((300,0))
        sizer_h2.Add(self.misclbl,0)
        sizer_h3.Add(self.nodestxt,1,flag=wx.ALL|wx.EXPAND, border=1)
        sizer_h3.Add(self.peerstxt,1,flag=wx.ALL|wx.EXPAND, border=1)
        sizer_h3.Add(self.misctxt,1,flag=wx.ALL|wx.EXPAND, border=1)
        # add the rest + sizer_h to the vertical sizer
        #sizer_v.Add(self.toolbar, 0, flag=wx.ALL|wx.EXPAND, border=10)
        sizer_v.Add(sizer_h1, 0, flag=wx.ALL|wx.EXPAND, border=10)
        sizer_v.Add(sizer_h, 0, flag=wx.ALL|wx.EXPAND, border=10)
        sizer_v.Add(self.lc, 3, flag=wx.ALL|wx.EXPAND, border=10)
        sizer_v.Add(self.lc2, 1, flag=wx.ALL|wx.EXPAND, border=10)
   
        sizer_v.Add(sizer_h2, 0, flag=wx.ALL|wx.EXPAND, border=10)
        sizer_v.Add(sizer_h3, 3, flag=wx.ALL|wx.EXPAND, border=10)
        self.SetSizer(sizer_v)



    def loadList1(self):
        self.lc.DeleteAllItems()
        self.lc2.DeleteAllItems()
        self.nodestxt.Clear()
        self.peerstxt.Clear()
        self.misctxt.Clear()
        counter=1

        #ipalias,idalias,transalias=[],[],[]#self.ip_id_trans_aliasing()
        #print transalias
        max_rows=len(self.list)
        
        for i,line in enumerate(self.list):
            index = self.lc.InsertStringItem(max_rows, str(counter))
            counter=counter+1
            #print line[1]
            if not(line[1]=='bogus')and not (line[0]=='bogus'):
                self.lc.SetStringItem(index, 1, str(line[0].ts))
                self.lc.SetStringItem(index, 2, str(line[1].ts))
                d=str(line[2])
                decimal.getcontext().prec = 4
                self.lc.SetStringItem(index, 3, str(d*1))
                self.lc.SetStringItem(index, 4, str(str(line[0].src_addr[0])
                                                    +':'+
                                                    str(line[0].src_addr[1])))
                self.lc.SetStringItem(index, 5, str(str(line[1].src_addr[0]))
                                      +':'+str(line[1].src_addr[1]))
                self.lc.SetStringItem(index, 6, str(line[0].hexaTid))
               
                #if line[0].sender_id in ipalias or line[1].sender_id in ipalias:
                if self.ip_alias == True:
                    self.lc.SetItemBackgroundColour(index,"plum")
                  
                #if line[0].src_addr[0] in idalias or line[1].src_addr[0] in idalias:
                if self.id_alias == True:
                    self.lc.SetItemBackgroundColour(index,"light green")
                                   
                #if line[0].hexaTid in transalias:
                if self.trans_alias == True:
                    self.lc.SetItemBackgroundColour(index,"yellow")
                if line[1].msg_type=='e':
                    self.lc.SetItemBackgroundColour(index,wx.RED)
            elif not (line[0]=='bogus')and (line[1]=='bogus'):
                self.lc.SetStringItem(index, 1, str(line[0].ts))
                self.lc.SetStringItem(index, 2, '-')
                self.lc.SetStringItem(index, 3, '-')
                self.lc.SetStringItem(index, 4, str(str(line[0].src_addr[0])
                                      +':'+str(line[0].src_addr[1])))
                self.lc.SetStringItem(index, 5, str(str(line[0].dst_addr[0]))
                                      +':'+str(line[0].dst_addr[1]))
                self.lc.SetStringItem(index, 6, str(line[0].hexaTid))
                self.lc.SetItemBackgroundColour(index,"light blue")
                #print line[0][0][0]

                #if line[0].sender_id in ipalias:
                if self.ip_alias == True:
                    self.lc.SetItemBackgroundColour(index,"plum") 
                 
                #if line[0].src_addr[0] in idalias:
                if self.id_alias == True:
                    self.lc.SetItemBackgroundColour(index,"light green")
                #if line[0].hexaTid in transalias:
                if self.trans_alias == True:
                    self.lc.SetItemBackgroundColour(index,"yellow")
        #self.list=self.QueResList  
            elif not (line[1]=='bogus')and (line[0]== 'bogus'):#response with no query
                self.lc.SetStringItem(index, 1, '-')
                self.lc.SetStringItem(index, 2, str(line[1].ts))
                self.lc.SetStringItem(index, 3, '-')
                self.lc.SetStringItem(index, 4, str(str(line[1].dst_addr[0])
                                      +':'+str(line[1].dst_addr[1])))
                self.lc.SetStringItem(index, 5, str(str(line[1].src_addr[0]))
                                      +':'+str(line[1].src_addr[1]))
                self.lc.SetStringItem(index, 6, str(line[1].hexaTid))
                self.lc.SetItemBackgroundColour(index,"light pink")
        self.ip_alias, self.id_alias, self.trans_alias = False,False,False
    def loadList2(self):
        pass
    
    def onClick(self,event):
        #print 'hello sara'
        id=0
        ipalias,transalias=[],[]#self.ip_id_trans_aliasing()
        mylist=[]
        thisclick=event.GetEventObject()

        if thisclick == self.id:
            #self.list == idalias
            idalias=self.ip_id_trans_aliasing(id=1)
            self.list=idalias
            self.id_alias = True
            self.loadList1()
        elif thisclick == self.ip:
            #print ipalias
            ipalias=self.ip_id_trans_aliasing(id=2)
            self.list=ipalias
            self.ip_alias=True
            self.loadList1()
        elif thisclick == self.tid:
            transalias=self.ip_id_trans_aliasing(id=3)
            for item in self.list:
                if item[0].hexaTid in transalias:
                    mylist.append(item)
            self.list=mylist
            self.trans_alias=True
            self.loadList1()
        elif thisclick == self.nores:
            objqnr=mainclass.MainClass()
            a=objqnr.query_with_no_response(self.QueResErrList)
            self.list=a
            self.no_res=True
            self.loadList1()
        elif thisclick == self.error:
            errlist=[]
            for item in self.QueResErrList:
                
                if not item[1]=='bogus' and item[1].msg_type == 'e':
                    errlist.append(item)
            self.list=errlist
            self.loadList1()


    def onSelect(self, event):

        ix_selected = self.lc.GetNextItem(item=-1,
            geometry=wx.LIST_NEXT_ALL, state=wx.LIST_STATE_SELECTED)
        qdistance='0'
        rdistance='0'
        Rsenderid='-'
        Qsenderid='-'
        qversion='-'
        rversion='-'
        type=''
        #QorR = str(self.list[ix_selected][4])

        if not (self.list[ix_selected][1]=='bogus'):
            Rtype= self.list[ix_selected][1].msg_type
            rversion=str(self.list[ix_selected][1].version)

        if not(self.list[ix_selected][1]=='bogus')and not Rtype == 'e' :
            Rsenderid = repr(self.list[ix_selected][1].sender_id)


        if not (self.list[ix_selected][0]=='bogus'):
            qversion = str(self.list[ix_selected][0].version)
            type = self.list[ix_selected][0].query_type
            Qsenderid = repr(self.list[ix_selected][0].sender_id)

        if type == 'get_peers'or type == 'announce_peer':
            qdistance = str(self.list[ix_selected][0].dist_from_sender)
            if not(self.list[ix_selected][1]=='bogus')and not Rtype == 'e':
                rdistance = str(self.list[ix_selected][1].dist_from_sender)
        else:
            qdistance = '0'
            rdistance= '0'
        self.lc2.DeleteAllItems()
        max_rows1=1
      

        index1= self.lc2.InsertStringItem(max_rows1,type)
        self.lc2.SetStringItem(index1,1,Qsenderid+' / '+qdistance)
        self.lc2.SetStringItem(index1,2,Rsenderid+' / '+rdistance)
        self.lc2.SetStringItem(index1,3,(str(qversion[0:2]) +'/'+str(rversion[0:2])))
        
        
        nodeval,peerval,miscval1,miscval2=self.nodes_text(ix_selected)
        self.nodestxt.Clear()
        self.peerstxt.Clear()
        self.misctxt.Clear()
        if nodeval:
            for i in range(len(nodeval)):
                self.nodestxt.WriteText(str(nodeval[i]))
      
        #self.nodestxt.WriteText(str(distval))
        self.peerstxt.WriteText(str(peerval))

        self.misctxt.WriteText(repr(miscval1))
        self.misctxt.WriteText('\n')
        self.misctxt.WriteText(repr(miscval2))

    def nodes_text(self,rownum):
        nodeval=''
        nodedist=''
        nodeaddr=''
        peerval=''
        miscval1=''
        miscval2=''
        value=''
        if not self.list[rownum][1]=='bogus':
            Rtype = self.list[rownum][1].msg_type
        if not (self.list[rownum][1]=='bogus')and not Rtype == 'e':
            
            if ( self.list[rownum][0].query_type=='get_peers'):
                #nodeval=str('NODES:'+'  '+ 
                #            str(self.list[rownum][1].nodes_address))
                #distval=str('DISTANCE:'+'   '+ 
                #            str(self.list[rownum][1].nodes_distances))
                nodelist=[]
                nodes_address=self.list[rownum][1].nodes_address
                for i in range(len(nodes_address)):       
                    nodeaddr=nodes_address[i]
                    nodedist=self.list[rownum][1].nodes_distances[i]
                    value = str(nodeaddr)+' '+'/'+' '+str(nodedist)+'\n'
                    #print value
                    nodelist.append(value)

                    #nodeval= str('NODES'+'  '+ str(nodelist))
                    nodeval = nodelist
                peerval= str(self.list[rownum][1].peers)
                miscval1=str('INFOHASH:'+'  ' +
                             repr(self.list[rownum][0].infohash))
                if self.list[rownum][1].token:
                    miscval2 = str('TOKEN:'+ '' + 
                                   repr(self.list[rownum][1].token))

                #if peerval == '0':
                    #peerval ='No Peers'
            
                
                return nodeval,peerval,miscval1,miscval2
            if self.list[rownum][0].query_type=='find_node':
                #nodeval= str('NODES'+'  '+ 
                        #     str(self.list[rownum][1].nodes_address))
                #distval=self.list[rownum][1].nodes_distances
                nodelist=[]
                nodes_address=self.list[rownum][1].nodes_address
                for i in range(len(nodes_address)):       
                    nodeaddr=nodes_address[i]
                    nodedist=self.list[rownum][1].nodes_distances[i]
                    value = str(nodeaddr)+' '+'/'+' '+str(nodedist)+'\n'
                    nodelist.append(value)
                    nodeval= nodelist
                miscval1= str('TARGET ID:'+'  '+ 
                                  repr(self.list[rownum][0].target_id))
                return nodeval,peerval,miscval1,miscval2
            if self.list[rownum][0].query_type=='announce_peer':
                #s1='no data'
                miscval1=str('PORT:'+' ' + 
                             str(self.list[rownum][0].btport))
                miscval2=str('TOKEN:'+' '+
                             str(self.list[rownum][0].token)+'  '
                             + 'INFOHASH:'+''
                             +repr(self.list[rownum][0].infohash))
                return nodeval,peerval,miscval1,miscval2
            if self.list[rownum][0].query_type=='ping':
                #s1= 'no data'
                
                return nodeval,peerval,miscval1,miscval2
        elif not (self.list[rownum][1]=='bogus')and (Rtype == 'e'):
            
            if self.list[rownum][0].query_type=='get_peers':
                miscval1=str('INFOHASH:'+'  ' +
                             repr(self.list[rownum][0].infohash))
                miscval2= str(self.list[rownum][1].error)
            if self.list[rownum][0].query_type=='find_node':  
                miscval1= str('TARGET ID:'+'  '+
                              repr(self.list[rownum][0].target_id))
                miscval2= str(self.list[rownum][1].error)
            if self.list[rownum][0].query_type=='announce_peer':
                #s1='no data'
                miscval1=str('PORT:'+' ' + 
                             str(self.list[rownum][0].btport))
                miscval2=str('TOKEN:'+' '+ 
                             str(self.list[rownum][0].token)+'  '
                             + 'INFOHASH:'+''
                             +repr(self.list[rownum][0].infohash)+' '
                             +'ERROR:'+''+str(self.list[rownum][1].error))
            return nodeval,peerval,miscval1,miscval2
        elif self.list[rownum][1]=='bogus':
            if self.list[rownum][0].query_type=='get_peers':
                miscval1=str('INFOHASH:'+'  ' +
                             repr(self.list[rownum][0].infohash))
                
            if self.list[rownum][0].query_type=='find_node':  
                miscval1= str('TARGET ID:'+'  '+
                              repr(self.list[rownum][0].target_id))
            if self.list[rownum][0].query_type=='announce_peer':
                #s1='no data'
                miscval1=str('PORT:'+' ' + 
                             str(self.list[rownum][0].btport))
                miscval2=str('TOKEN:'+' '+ 
                             str(self.list[rownum][0].token)+'  '
                             + 'INFOHASH:'+''
                             +repr(self.list[rownum][0].infohash))
                          
            return nodeval,peerval,miscval1,miscval2
        #elif self.list[rownum][0]=='bogus'and Rtype =='e':
         #   miscval1 = self.list[rownum][0].error
          #  return nodeval,peerval,miscval1,miscval2

        #elif self.list[rownum][0]=='bogus':
         #   return nodeval,peerval,miscval1,miscval2
        else:
            return nodeval,peerval,miscval1,miscval2
    def createmenu(self):
	    
        menubar = wx.MenuBar()

        file = wx.Menu()
        edit = wx.Menu()
        capture=wx.Menu()
        statistics=wx.Menu()
        queryandres=wx.Menu()
        filters=wx.Menu()
        lookup=wx.Menu()
        graphs=wx.Menu()
        help = wx.Menu()


        file.Append(101, '&Open', 'Open a new document')
        file.Append(102, '&Save', 'Save the document')
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        file.AppendItem(quit)
        

        edit.Append(106, 'Cut\tCtrl+Q', 'Cut the text')
        edit.Append(107, '&Copy\tCtrl+C', 'Copy the text')
        edit.Append(108, 'Paste\tCtrl+V', 'Paste the text')

        
        
        capture.Append(109, 'Start Capture', 'Live Capture')
        capture.Append(110, 'Stop Capture', 'Stop Capture')
        #queries.Append(111, 'Find_node', 'Find_node queries')
        #queries.Append(112, 'Announce_peer', 'Announce_peer queries')
        #queries.Append(113, 'Ping', 'Ping Queries')

        statistics.Append(114, 'Statistics', 'Statistics')
        #responses.Append(115, 'Get_peers', 'Get_peers responses')
        #responses.Append(116, 'Find_node', 'Find_node responses')
        #responses.Append(117, 'Announce_peer/Ping', 'Announce_peer/Ping responses')


        queryandres.Append(118, 'All QandR', 'All queries and responses')
        queryandres.Append(119, 'Get_peers QandR',
                           'Get_peers query and response')
        queryandres.Append(120, 'Find_node QandR',
                           'Find_node query and response')
        queryandres.Append(121, 'Announce_peer QandR', 
                           'Announce_peer queryand response')
        queryandres.Append(122, 'Ping QandR', 'Ping query and response')
        queryandres.Append(130, 'Query with no response', 
                           'Queries having no response')
        queryandres.Append(131, 'Response with no query', 
                           'Responses having no query')


        filters.Append(123, 'Filters', 'select filters')
        
        lookup.Append(124, 'Lookup', 'Lookup Converge Overview')

        graphs.Append(125, 'Graphs', 'Show graphs')
        
        help.Append(126, 'About Look@kad', 'Show Help')
        
     


        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(capture, 'Capture')
        menubar.Append(queryandres,'Query and Response')
        menubar.Append(filters, 'Filters')
        menubar.Append(lookup, 'Lookup')
        menubar.Append(statistics, 'Statistics')
        menubar.Append(graphs, 'Graphs')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()

    def createToolBar(self):
        #vbox = wx.BoxSizer(wx.VERTICAL)
       

        self.toolbar = wx.ToolBar(self, style=wx.TB_HORIZONTAL|wx.TB_TEXT)
        #self.toolbar.SetToolBitmapSize((10,10))
        self.toolbar.SetFont(wx.Font(5, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        
        self.toolbar.AddLabelTool(1, "Open",
            wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR))
        self.toolbar.AddLabelTool(2, "Capture",
            wx.Bitmap('images/capture.png'))
        self.toolbar.AddLabelTool(3, "Quit",
            wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR))
        self.toolbar.AddLabelTool(4, "Lookup",
            wx.Bitmap('images/lookup.png'))
        self.toolbar.AddLabelTool(5, "Filter",
            wx.Bitmap('images/filter.png',))
        self.toolbar.AddLabelTool(6, "Statistics",
            wx.Bitmap('images/statistics.png'))
        self.toolbar.AddLabelTool(7, "Graphs",
            wx.Bitmap('images/graph.png'))
        self.toolbar.AddLabelTool(8, "Help",
            wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR))
        #self.toolbar.SetSize(wx.Size(60, 60))
        self.toolbar.Realize()
        self.SetToolBar(self.toolbar)
        #self.Centre()

    def onSortRTT(self, event):
        rtt_index = operator.itemgetter(3)
        self.list.sort(key=rtt_index)
        self.loadList1()

    def onListColClick(self, event):
       
        #event.Skip()
        col = event.GetColumn()
        print 'column clicked',col
        if col == 1:
            #if self.col1toggled==True:
            #    for i,line in enumerate(self.list):
             #       self.lc.SetStringItem(i, 1,str(line[0].ts))
              #  self.col1toggled=False
            #else:
             #   for i,line in enumerate(self.list):
              #      self.lc.SetStringItem(i, 1,str(line[0].absTs))
               # self.col1toggled=True
            qts_index = operator.itemgetter(0)
            if self.col1toggled == True:           
                self.list.sort(key=qts_index)
                self.col1toggled=False

            else:
                self.list.sort(key=qts_index, reverse=True)
                self.col1toggled=True
            self.loadList1()

        elif col == 2:

            #if self.col2toggled==True:
               # for i ,line in enumerate(self.list):
               #     if not line[1]=='bogus':
              #          self.lc.SetStringItem(i, 2,str(line[1].ts))
             #   self.col2toggled=False
            #else:
                #for i,line in enumerate(self.list):
                #    if not line[1]=='bogus':
               #         self.lc.SetStringItem(i, 2,str(line[1].absTs))
              #self.col2toggled=True

            rts_index = operator.itemgetter(1)
            if self.col2toggled == True:           
                self.list.sort(key=rts_index)
                self.col2toggled=False

            else:
                self.list.sort(key=rts_index, reverse=True)
                self.col2toggled=True
            self.loadList1()


        elif col == 6:
            if self.col6toggled==True:
                for i,line in enumerate(self.list):
                    self.lc.SetStringItem(i, 6, str(line[0].hexaTid))
                self.col6toggled=False
            else:
                for i,line in enumerate(self.list):
                    self.lc.SetStringItem(i, 6, repr(line[0].tid))
                self.col6toggled=True

        elif col == 3:
            rtt_index = operator.itemgetter(2)
            if self.col3toggled == False:
 
            
                self.list.sort(key=rtt_index)
                self.col3toggled=True

            else:
                self.list.sort(key=rtt_index, reverse=True)
                self.col3toggled=False
            self.loadList1()

    def onRightClick(self,event):
        ix_selected = self.lc.GetNextItem(item=-1,
            geometry=wx.LIST_NEXT_ALL, state=wx.LIST_STATE_SELECTED)
        source=str(self.list[ix_selected][0][0])
        #print source
        #print destination

app = wx.App(0)

mytitle = "Kademlia Lookup Analyzer-Look@Kad"
width = 580
height = 360

Gui(None, mytitle, (width, height)).Show()
app.MainLoop()

       


