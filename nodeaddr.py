# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information
#!/usr/bin/python

# plot.py

import wx

import pygeoip


GEOIP_FILENAME = 'GeoIP/GeoIP.dat'


class Nodes(wx.Dialog):




        def __init__(self, parent,title,nodesaddr,nodesdist,size):
                wx.Dialog.__init__(self, parent, wx.ID_ANY, title, size)

		self.gi = pygeoip.GeoIP(GEOIP_FILENAME)
		self.addresses=[]
		self.list=[]
		self.distances =nodesdist 
		self.addresses=nodesaddr

		for i in range(len(self.addresses)):
			location=self.gi.country_name_by_addr(
                                self.addresses[i][0])
			#isp = self.gio.org_by_addr(self.addresses[i][0])
			self.list.append((self.addresses[i],location))

		self.addrtxt = wx.TextCtrl(self, size=wx.Size(200, -1),
					   value=str(self.list),
					   style=wx.TE_MULTILINE)
	
		
	
		#print self.addresses[0]
        def OnQuit(self, event):
                self.Destroy()

