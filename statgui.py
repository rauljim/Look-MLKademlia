# Copyright (C) 2010 Sara Dar
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information
import wx
#import queriesgiven as qr
#import responsegiven as re
import statistics as stat


class StatGui(wx.Dialog):
    def __init__ (self, parent, title,qls,rls,qrls,srcaddr,mysize):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,title, mysize)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        heading = wx.StaticText(self, -1, 'Quick View', (150, 30))
        heading.SetFont(font)
        
        src_addr=srcaddr
        self.qlist=qls
        self.rlist=rls
        self.qrlist=qrls
        self.srcTxt= wx.TextCtrl(self, size=wx.Size(100, 40),
                                  value=src_addr)
   
        #if self.src_addr:
        #    self.srcTxt.setValue(self.src_addr)
     

      
       
        wx.Button(self, 1, 'Ok',(100, 0))
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=1)
      

    def OnOk(self, event):
        self.create_controls()

    def create_controls(self):

        src_add = self.srcTxt.GetValue()
        obj=stat.Stats()

        #print self.qlist,self.rlist
        qsent,qrecv,rsent,rrecv,avgRtt=obj.data_collector(src_add,
                                                   self.qlist,
                                                   self.rlist,self.qrlist)
        #print qsent,qrecv
        
        wx.StaticLine(self, -1, (25, 50), (300,1))
        wx.StaticText(self, -1, 'Queries Sent', (25, 100), style=wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, 'Responses Received', (25, 120), 
                      style=wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, 'Queries Received', (25, 140))
        wx.StaticText(self, -1, 'Responses Sent', (25, 160))
        #wx.StaticText(self, -1, '', (25, 180))
        wx.StaticText(self, -1, 'Average RTT', (25, 180))
        wx.StaticText(self, -1, 'Generated Msg/Recieved Msg',
                      (25, 220))
        wx.StaticText(self, -1, str(qsent), (250, 100))
        wx.StaticText(self, -1, str(rrecv), (250, 120))
        wx.StaticText(self, -1, str(qrecv), (250, 140))
        wx.StaticText(self, -1, str(rsent), (250, 160))
        wx.StaticText(self, -1, str(avgRtt), (250, 180))
        wx.StaticText(self, -1, str(qsent+rsent)+'/'+str(
                qrecv+rrecv), (250, 220))
 
        wx.StaticLine(self, -1, (25, 260), (300,1))
        self.Centre()
       
                
       

    def populate_controls(self): 

      
        pass
       





"""class MyApp(wx.App):
    def OnInit(self):
        dia = MyDialog(None, -1, 'Look@Kad')
        dia.ShowModal()
        dia.Destroy()
        return True

app = MyApp()
app.MainLoop()
"""
