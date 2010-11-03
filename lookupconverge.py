# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information
import wx
import os
import sys
import decimal
import operator
import nodeaddr as NodeAddr
import pickle
#import queriesgiven as q
#import responsegiven as r
#import matchqandr as qr
#import mappings as map

class LookupConverge(wx.Frame):
    fname=''
    srctxt=''
    infotxt=''
    infohash=''
    #infohashlist=[]
    
    Qrecord=[]
    Rrecord=[]
    newResList=[]
    list=[]
    QueResList=[]
    
    def __init__(self, parent, mytitle,qrlist, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle,
            size=(1000,800))
        #self.m=map.Mappings()
        #self.fname=filename
        self.infohash=''
        #self.infohashlist=infohashlist
        self.newResList=[]
        self.QueResList=qrlist
        self.CreateStatusBar()
        self.create_controls()
        #unpicklefile = open('myfile.txt', 'r')

# now load the list that we pickled into a new object
        #self.list = pickle.load(unpicklefile)

# close the file, just for safety
        #unpicklefile.close()



        self.bindings()

        
    def bindings(self):
        #self.Bind(wx.EVT_BUTTON, self.open_file, id=1)
        self.Bind(wx.EVT_BUTTON, self.collect_values, id=2)
        self.Bind(wx.EVT_BUTTON, self.close_dlg, id=3)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelect)
        self.lc.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.onRightClick)        


    def load_list(self):
        self.lc.DeleteAllItems()


        #self.fname=self.filetxt.GetValue()
        #source=self.srctxt.GetValue()
        #infoh=self.infobox.GetValue()


        #a=qr.MatchQandR(self.fname)
        #b=r.ResponseBisector(self.fname,infoh)
        counter=1
        start=0
        previousts=0
        distList=[]
        
        #self.Qrecord = a.get_peers_with_srcaddr_infohash(source,infoh)
        #self.Rrecord = b.get_peers_response()
        #self.list =a.get_peers_query_response_inline_with_src_infohash(source,infoh)
        #self.text.Clear()
        
        counter=1
       
        max_rows=len(self.list)
       
        for i,line in enumerate(self.list):
            #print 'hello'
            index = self.lc.InsertStringItem(max_rows, str(counter))
            counter=counter+1
            if not(line[1]=='bogus'):

        
                self.lc.SetStringItem(index, 1, str(line[0].ts))
                self.lc.SetStringItem(index, 2, str(line[1].ts))
                #d=decimal.Decimal(str(line[1].ts-line[0].ts))
                d=str(line[2])
                decimal.getcontext().prec = 4
                self.lc.SetStringItem(index, 3, str(d*1))
              
                self.lc.SetStringItem(index, 4, str(str(line[1].src_addr[0]))
                                      +':'+str(line[1].src_addr[1]))
                self.lc.SetStringItem(index, 5, str(line[0].hexaTid))
                self.lc.SetStringItem(index,6,
                                      str(str(line[0].dist_from_sender)
                                      +'/'+str(line[1].dist_from_sender)))
                self.lc.SetStringItem(index,7,str(line[1].nodes_distances))
                #print line[1].ts
                #if d < 0:
                    #self.lc.SetItemBackgroundColour(index,wx.RED)
                self.newResList.append(line)
                #self.lc.SetItemBackgroundColour(index,wx.RED)
            else:
                self.lc.SetStringItem(index, 1, str(line[0].ts))
                self.lc.SetStringItem(index, 2, '-')
                self.lc.SetStringItem(index, 3, '-')
                self.lc.SetStringItem(index, 4,str(str(line[0].dst_addr[0])
                                      +':'+str(line[0].dst_addr[1]))) 
                self.lc.SetStringItem(index, 5, str(line[0].hexaTid))
                self.lc.SetItemBackgroundColour(index,'light blue')
                self.newResList.append(line)
                    

    def create_controls(self):
	"""Called when the controls on Window are to be created"""
        # Create the static text widget and set the text
	#self.filelabel = wx.StaticText(self, label="File:")
        self.srclabel = wx.StaticText(self, label="Source Addr:")
        self.infolabel = wx.StaticText(self, label="Infohash:")
        self.peerslabel = wx.StaticText(self,label="Peers")
	#Create the Edit Field (or TextCtrl)
	#self.filetxt = wx.TextCtrl(self, size=wx.Size(200, -1),
                                                      #value=self.fname)
        self.srctxt = wx.TextCtrl(self, size=wx.Size(100, -1),
                                  value='192.16.125.181')
        self.infotxt = wx.TextCtrl(self, size=wx.Size(100, -1),
                                   value='3ef5cdcbcf57fecf0da0be4cff8d90fee1369649')
#28f2e5ea2bf87eae4bcd5e3fc9021844c01a4df9
        #self.browsebtn=wx.Button(self, 1, 'Browse', (50, 130))
        self.Okbtn=wx.Button(self, 2, 'OK    ', (50, 130))
        self.Cancelbtn=wx.Button(self, 3, 'Cancel', (50, 130))


        #create list cotrol

        self.lc = wx.ListCtrl(self, wx.ID_ANY,
        style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES)
        self.lc.InsertColumn(0,"No.")
        self.lc.SetColumnWidth(0, 40)
        self.lc.InsertColumn(1,"Query Time")
        self.lc.SetColumnWidth(1, 120)
        self.lc.InsertColumn(2,"Response Time")
        self.lc.SetColumnWidth(2, 120)
        self.lc.InsertColumn(3,"RTT")
        self.lc.SetColumnWidth(3,80 )
        self.lc.InsertColumn(4,"Responder")
        self.lc.SetColumnWidth(4, 160)
        self.lc.InsertColumn(5,"TID")
        self.lc.SetColumnWidth(5, 60)
       
        self.lc.InsertColumn(6,"Log Distance")
        self.lc.SetColumnWidth(6, 100)
        self.lc.InsertColumn(7,"Nodes Distance")
        self.lc.SetColumnWidth(7, 260)

        #self.loadList()
        self.text = wx.TextCtrl(self, wx.ID_ANY,
            value="PEERS",
            style=wx.TE_MULTILINE)




	# Horizontal sizer
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
	self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        #vertical sizer
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
	#Add to horizontal sizer
	#add the static text to the sizer, tell it not to resize
	#self.h_sizer1.Add(self.filelabel, 0)
	#Add 5 pixels between the static text and the edit
        #self.h_sizer1.AddSpacer((5,0))
        #self.h_sizer1.Add(self.filetxt,0)
        #self.h_sizer1.AddSpacer((5,0))
        #self.h_sizer1.Add(self.browsebtn, 0)

        self.h_sizer2.Add(self.srclabel,0)
        self.h_sizer2.AddSpacer((5,0))
        self.h_sizer2.Add(self.srctxt,1)

        self.h_sizer3.Add(self.infolabel,0)
        self.h_sizer3.AddSpacer((5,0))
        self.h_sizer3.Add(self.infotxt,1)
        
        self.h_sizer4.Add(self.Okbtn,0)
        self.h_sizer4.AddSpacer((5,0))
        self.h_sizer4.Add(self.Cancelbtn,0)
        
        self.h_sizer5.Add(self.lc, 3, flag=wx.ALL|wx.EXPAND, border=10)
        self.h_sizer6.Add(self.peerslabel,0)
        self.h_sizer7.Add(self.text, 3, flag=wx.ALL|wx.EXPAND, border=10)

        self.v_sizer.Add(self.h_sizer0,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer1,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer2,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer3,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer4,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer5,1,wx.ALL|wx.EXPAND,border=10)
        self.v_sizer.Add(self.h_sizer6,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer7,0,wx.ALL|wx.EXPAND,border=10)
	#Set the sizer
	self.SetSizer(self.v_sizer)


    
    def onSelect(self, event):

        ix_selected = self.lc.GetNextItem(item=-1,
            geometry=wx.LIST_NEXT_ALL, state=wx.LIST_STATE_SELECTED)
        self.text.Clear()
        if not self.newResList[ix_selected][1]=='bogus':
            peers = str(self.newResList[ix_selected][1].peers)
        #print peers

            self.text.WriteText(str(peers))

    def onRightClick(self,event):
        ix_selected = self.lc.GetNextItem(item=-1,
            geometry=wx.LIST_NEXT_ALL, state=wx.LIST_STATE_SELECTED)
       
        nodesaddr = (self.newResList[ix_selected][1].nodes_address)
        nodesdist = str(self.newResList[ix_selected][1].nodes_distances)
        #print peers
        width = 1000
        height = 800
        obj=NodeAddr.Nodes(None, 'Nodes Addresses',nodesaddr,nodesdist, 
                               (width, height)).Show()

    

    def collect_values(self,event):
        #fname=self.filetxt.GetValue()
        source=self.srctxt.GetValue()
        infoh=self.infotxt.GetValue()
        self.list_with_src_infohash(source,infoh)
        self.load_list()
        # import the pickle module


# lets create something to be pickled
# How about a list?
        #picklelist = ['one',2,'three','four',5,'can you count?']

# now create a file
# replace filename with the file you want to create
#        file = open('myfile.txt', 'w')

# now let's pickle picklelist
#        pickle.dump(self.list,file)

# close the file, and your pickling is complete
#        file.close()

    def list_with_src_infohash(self,source,infoh):
        self.list=[]
        for i in range(len(self.QueResList)):
            if self.QueResList[i][0].query_type == 'get_peers':
                if self.QueResList[i][0].src_addr[0]==source:
                    if repr(self.QueResList[i][0].infohash)==infoh:
                        self.list.append(self.QueResList[i])
         
        #self.load_list()

    def close_dlg(self,event):
        self.Destroy()

    def show_message(self):
        dlg = wx.MessageDialog(self,'Check src address and infohash',
                                   'Error', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def match_nodeaddr_responder(self):
        pass


#app = wx.App(0)
#set title and size for the MyFrame instance
#mytitle = "Lookup Overview for...."
#width = 580
#height = 36
#LookupConverge(None, mytitle, (width, height)).Show()

#app.MainLoop()
