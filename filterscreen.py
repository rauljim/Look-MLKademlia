# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information

import wx
import operator
import os
import sys
import filters


class FilterScreen(wx.Frame):
    
    src=''
    dst=''
    tid=''
    parent=''

    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle,
            size=mysize)
        self.create_controls()
        self.bindings()
        self.parent = parent

    def create_controls(self):
        """Called when the controls on Window are to be created"""
        # Create the static text widget and set the text
        self.parameter_list = [
            'src','dst','tid','data','srcport','dstport','qts','rts','RTT','token','infohash']
        self.paramlist = wx.ListBox(self, 20, wx.DefaultPosition, (170, 130), self.parameter_list, wx.LB_SINGLE)

        self.operator_list = ['==','!=','>=','<=','>','<']
        self.keyword_list = ['and','or']

        self.operatorlist = wx.ListBox(self, 21, wx.DefaultPosition, (170, 130), self.operator_list, wx.LB_SINGLE)
        
        self.keywordlist = wx.ListBox(self, 22, wx.DefaultPosition, (170, 130), self.keyword_list, wx.LB_SINGLE)
        self.paramlbl = wx.StaticText(self,label="Filters")
     
        self.filtertxt = wx.TextCtrl(self, size=wx.Size(200, -1),
                                                      value='')
        self.Okbtn=wx.Button(self, 2, 'OK    ', (50, 130))
        self.Cancelbtn=wx.Button(self, 3, 'Cancel', (50, 130))


	# Horizontal sizer
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
	self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
      	self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
       # self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        #vertical sizer
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
	#Add to horizontal sizer
        self.h_sizer0.AddSpacer((20,0))
        self.h_sizer0.Add(self.paramlbl,0)
        self.h_sizer1.AddSpacer((20,0))
        self.h_sizer1.Add(self.paramlist,0,wx.ADJUST_MINSIZE,0)
        self.h_sizer1.AddSpacer((20,0))
        self.h_sizer1.Add(self.operatorlist,0,wx.ADJUST_MINSIZE,0)
        self.h_sizer1.AddSpacer((20,0))
        self.h_sizer1.Add(self.keywordlist,0,wx.ADJUST_MINSIZE,0)



        self.h_sizer2.Add(self.filtertxt,1)
        self.h_sizer3.Add(self.Okbtn,0)
        self.h_sizer3.AddSpacer((12,0))
        self.h_sizer3.Add(self.Cancelbtn,0)
       
        self.v_sizer.Add(self.h_sizer0,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer1,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer2,0,wx.EXPAND|wx.BOTTOM,10)
        self.v_sizer.Add(self.h_sizer3,0,wx.EXPAND|wx.BOTTOM,10)
      
	#Set the sizer
	self.SetSizer(self.v_sizer)


    def bindings(self):
        self.Bind(wx.EVT_BUTTON, self.send_values, id=2)
        self.Bind(wx.EVT_BUTTON, self.close_dlg, id=3)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect1, id=20)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect2, id=21)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect3, id=22)
    def OnSelect1(self, event):
        index = event.GetSelection()
        parameter = self.paramlist.GetString(index)
        self.filtertxt.AppendText(' '+parameter +' ')


    def OnSelect2(self, event):
        index = event.GetSelection()
        operator = self.operatorlist.GetString(index)
        self.filtertxt.AppendText(' '+operator+ ' ')

    def OnSelect3(self, event):
        index = event.GetSelection()
        kword = self.keywordlist.GetString(index)
        self.filtertxt.AppendText(''+kword+ ' ')


    def close_dlg(self,event):
        self.Destroy()


    def send_values(self,event):
        
        values=self.filtertxt.GetValue()
        fobj=filters.Filters()
        f= fobj.check_filter_validity(values)
        if f==True:
            self.parent.get_filter_values(values)
            self.Destroy()
        else:
            textstyle = wx.TextAttr()
            textstyle.SetBackgroundColour(wx.RED)
            self.filtertxt.SetDefaultStyle(textstyle)
            self.filtertxt.AppendText(' ')
        

