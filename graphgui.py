# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information
#!/usr/bin/python

# plot.py

import wx
import wx.lib.plot as plot
import decimal
import pymdht.core.identifier as identifier
import graphs
class GraphGui(wx.Frame):

	list=[]
	data=[]

	
        def __init__(self, parent,title,qrlist,size):
                wx.Frame.__init__(self, parent, wx.ID_ANY, title,size)

                self.da = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (10,10)]
		self.data=[]
		self.list = qrlist
		#txt = wx.TextCtrl
		self.create_controls()
		self.create_bindings()
		self.min=0
		self.max=0
		#self.btn1.Disbale()
		#self.btn2.Disable()
		self.trafficbtn.Disable()
		self.qrbtn.Disable()
		self.convergebtn.Disable()
		#self.dlist=[]
		self.infotxt.Disable()
		self.rttselected=True
		self.trafselected=False
		self.gpcount=0
		self.fncount=0
		self.pcount=0
		self.apcount=0
		

	def create_controls(self):
		self.typeList=['All','get_peers', 
			       'find_node','ping','announce_peer']
		self.statusbar = self.CreateStatusBar(1)
		self.graphlbl = wx.StaticText(self,label="Select Graph:")
		self.rttopt = wx.RadioButton(self, -1, 'RTT',
					  (10, 10), style=wx.RB_GROUP)
		self.trafficopt = wx.RadioButton(self, -1, 'Traffic', (10, 30))

		self.qropt = wx.RadioButton(self, -1, 'Q and R', (10, 30))
		self.convergeopt = wx.RadioButton(self, -1, 
						  'Convergence', (10, 30))
		self.srclbl = wx.StaticText(self,label="Source Address")
		self.srctxt = wx.TextCtrl(self, size=wx.Size(200, -1),
					  value='192.16.125.181')
		self.typelbl = wx.StaticText(self,label="Data Type")
		self.typebox = wx.ComboBox(self, size=wx.Size(150, -1),
                                   choices=self.typeList,value='Select Type')
		self.infolbl = wx.StaticText(self, label="Infohash:")
		self.infotxt = wx.TextCtrl(self, size=wx.Size(350, -1),
                        value='3ef5cdcbcf57fecf0da0be4cff8d90fee1369649')
		self.qrbtn = wx.Button(self,  1, 'Q and R', (50,50))
                self.rttbtn = wx.Button(self,  2, 'RTT', (50,90))
                self.trafficbtn = wx.Button(self,  3, 'Traffic', (50,130))
		self.convergebtn = wx.Button(self,  4, 'Convergence', (50,170))
                self.quitbtn = wx.Button(self,  5, 'quit', (50,210))
		

		sizer_v = wx.BoxSizer(wx.VERTICAL)
		sizer_h0 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h0.Add(self.graphlbl,0)
		sizer_h0.Add(self.rttopt,0)
		sizer_h0.Add(self.trafficopt,0)
		sizer_h0.Add(self.qropt,0)
		sizer_h0.Add(self.convergeopt,0)
		sizer_h.Add(self.srclbl,0)
		sizer_h.Add(self.srctxt,0)
		sizer_h1.Add(self.typelbl,0)
		sizer_h1.Add(self.typebox,0)
		sizer_h2.Add(self.infolbl,0)
		sizer_h2.Add(self.infotxt,0)

		sizer_h3.Add(self.rttbtn,0)
		
		sizer_h3.Add(self.trafficbtn,0)
		sizer_h3.Add(self.qrbtn,0)
		sizer_h3.Add(self.convergebtn,0)
		sizer_h3.Add(self.quitbtn,0)
		sizer_v.Add(sizer_h0,0,wx.EXPAND|wx.BOTTOM,10)
		sizer_v.Add(sizer_h,0,wx.EXPAND|wx.BOTTOM,10)
		sizer_v.Add(sizer_h1,0,wx.EXPAND|wx.BOTTOM,10)
		sizer_v.Add(sizer_h2,0,wx.EXPAND|wx.BOTTOM,10)
		sizer_v.Add(sizer_h3,0,wx.EXPAND|wx.BOTTOM,10)
		self.SetSizer(sizer_v)


	def create_bindings(self):
		wx.EVT_BUTTON(self, 1, self.OnQandR)
                wx.EVT_BUTTON(self, 2, self.OnRTT)
                wx.EVT_BUTTON(self, 3, self.OnTraffic)
		wx.EVT_BUTTON(self, 4, self.OnConvergence)
                wx.EVT_BUTTON(self, 5, self.OnQuit)
                wx.EVT_CLOSE(self, self.OnQuit)
		self.Bind(wx.EVT_COMBOBOX, self.OnSelect)

		self.Bind(wx.EVT_RADIOBUTTON, self.Onrtt_opt,
			  id=self.rttopt.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.Ontraffic_opt,
			  id=self.trafficopt.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.Onqr_opt,
			  id=self.qropt.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.Onconverge_opt,
			  id=self.convergeopt.GetId())
	def OnSelect(self, event):
		#print 'in onslect'
		item = event.GetSelection()
		#print item
		#if get_peers is selected
		if item == 1:
			self.infotxt.Enable()
		else:
			self.infotxt.Disable()
	def Onrtt_opt(self, event):
		self.trafficbtn.Disable()
		self.qrbtn.Disable()
		self.convergebtn.Disable()
		self.rttbtn.Enable()
		#self.infotxt.Enable()
		self.typebox.Enable()
		self.rttselected=True
		#self.trafselected=False

	def Ontraffic_opt(self,event):
		self.trafficbtn.Enable()
		self.rttbtn.Disable()
		self.qrbtn.Disable()
		self.convergebtn.Disable()
		self.infotxt.Disable()
		self.typebox.Disable()
		#self.rttselected=False
		self.trafselected=True

	def Onqr_opt(self,event):
		self.qrbtn.Enable()
		self.rttbtn.Disable()
		self.trafficbtn.Disable()
		self.convergebtn.Disable()
		self.infotxt.Disable()
		self.typebox.Enable()
		#self.rttselected=False
		#self.qrselected=True

	def Onconverge_opt(self,event):
		self.convergebtn.Enable()
		self.rttbtn.Disable()
		self.trafficbtn.Disable()
		self.qrbtn.Disable()
		self.infotxt.Enable()
		self.typebox.Disable()
		#self.rttselected=False
		#self.trafselected=True

        def OnQandR(self, event):

		frm = wx.Frame(self, -1, 'Look@MLKademlia', size=(600,450))
		client = plot.PlotCanvas(frm)
		client.SetEnableZoom(True)
		source=self.srctxt.GetValue()
		infoh = self.infotxt.GetValue()
		type=self.typebox.GetValue()
		thisclick= event.GetEventObject()

		obj=graphs.Plot()

		qts,rts=obj.timestamps(self.list,source,infoh,type)
		if not qts:
			print 'no queries found'
			assert 0
		a = min(qts)
		b= max(qts)
		minimum = a[1]-1
		maximum =  b[1]+1
		

		client.SetEnableLegend(True)
		client.SetEnableGrid(True)
		markers1 = plot.PolyMarker(qts, 
					   legend='Query', colour='red',
					   marker='circle', size=1,width=1)
		markers2 = plot.PolyMarker(rts, 
					   legend='Response', colour='blue',
					   
					   marker='triangle', size=1,width=1)
          
		gc = plot.PlotGraphics([markers1,markers2],
				       'Queries and Responses', 'Queries and Responses', 'Time(s)')
		
	
		client.Draw(gc, xAxis=(0,len(qts)), yAxis=(minimum,maximum))
		
	
                frm.Show(True)

			
        def OnRTT(self, event):
		m1=0
		m2=0
		newdata=[]
		source=self.srctxt.GetValue()
		type = self.typebox.GetValue()
		infoh = self.infotxt.GetValue()
		obj=graphs.Plot()
		data=obj.get_rtt_data(self.list,source,type,infoh)
		cum,values=obj.cdf(data)
		for c,v in zip(cum,values):
			newdata.append((v,c))
	
                frm = wx.Frame(self, -1, 'Look@MLKademlia', size=(600,450))
                client = plot.PlotCanvas(frm)
		client.SetEnableZoom(True)
                line = plot.PolyLine(newdata, legend='', colour='red', width=1)
		#marker = plot.PolyMarker(self.data, marker='dot')
                gc = plot.PlotGraphics([line], 
				       'Round Trip Time', 'RTT (s)', 'CDF')
		print client.getLogScale()
                client.Draw(gc,  xAxis= (0,3), yAxis= (0,1))
		#client.Draw(gc)
                frm.Show(True)

        def OnConvergence(self, event):
		m1=0
		m2=0
		newdata=[]
		#self.get_rtt_data()
		source=self.srctxt.GetValue()
		infoh = self.infotxt.GetValue()
		obj=graphs.Plot()
		newdata=obj.convergence(self.list,source,infoh)
		firstitem=[]
		for item in newdata:
			firstitem.append(item[0])
			
		if firstitem:
			maxi=max(firstitem)
			mini=min(firstitem)
                frm = wx.Frame(self, -1, 'Look@MLKademlia', size=(600,450))
                client = plot.PlotCanvas(frm)
		client.SetEnableZoom(True)
                line = plot.PolyLine(newdata, legend='', colour='red', width=1)
		marker = plot.PolyMarker(newdata, marker='triangle',
					 colour='blue',size=1,width=1)
                gc = plot.PlotGraphics([line,marker], 
				       'Lookup Convergence','Time(s)', 
				       'Log Distance from Infohash')
                client.Draw(gc,  xAxis= (mini-1,maxi+1),
			    yAxis= (100,180))
		#client.Draw(gc)
                frm.Show(True)



	def OnTraffic(self, event):

		source=self.srctxt.GetValue()
		obj=graphs.Plot()
		
		gpcount,fncount,pcount,apcount=obj.get_traffic_data(self.list,
								    source)
                frm = wx.Frame(self, -1, 'Look@MLKademlia', size=(600,450))
                client = plot.PlotCanvas(frm)
                bar1 = plot.PolyLine([(1, 0), (1,gpcount)],
				     legend=u"get_peers", 
				     colour='green', width=25)
                bar2 = plot.PolyLine([(3, 0), (3,fncount)],
				     legend="find_node",
				     colour='blue', width=25)
                bar3 = plot.PolyLine([(5, 0), (5,pcount)],
				     legend="Ping", 
				     colour='yellow', width=25)
                bar4 = plot.PolyLine([(6, 0), (6,apcount)],
				     legend="announce_peer", 
				     colour='orange', width=25)
                gc = plot.PlotGraphics([bar1, bar2, bar3, bar4],
				       'Total traffic Generated',
				       'Messages Type', 'No. of Messages')
		client.SetEnableLegend(True)
                client.Draw(gc, xAxis=(0,10), yAxis=(0,len(self.list)))
                frm.Show(True)



        def OnQuit(self, event):
                self.Destroy()

