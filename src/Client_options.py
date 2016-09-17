import wx
import socket
import Client
import threading
import image_detection as web_cam
import re

class Options(wx.Frame):
    def __init__(self, parent, title):
        super(Options, self).__init__(parent, title=title, size=(400, 250))
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour("black")
        self.panel.SetForegroundColour("white")
        self.start = wx.Button(self.panel, id=wx.ID_ANY, label="Start", pos=(250, 150))
        self.Bind(wx.EVT_BUTTON, self.start_server_fn, self.start)
        self.webcam = wx.Button(self.panel, id=wx.ID_ANY, label="Test Webcam", pos=(250, 100))
        self.Bind(wx.EVT_BUTTON, self.webcam_fn, self.webcam)
        self.ip = wx.StaticText(self.panel, -1, label="IP address:" , pos=(10, 20), name='ip')

        self.ip_address = wx.TextCtrl(self.panel, -1, pos=(100, 20))
        self.ip_address.SetLabel('127.0.0.1')

        self.color_s_l = wx.StaticText(self.panel, -1, label="Client Color:", pos=(10, 55), name='color')
        self.color_select_s = wx.ColourPickerCtrl(self.panel, id=wx.ID_ANY, pos=(100, 55))
        self.color_select_s.SetColour((0, 0, 255))

        self.SetTitle('Client')
        self.Centre()
        self.Show(True)

    def start_server_fn(self, event):
        m = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.ip_address.GetValue())
        if (m == None):
            msgbox = wx.MessageBox('IP address not vaild',
                                   'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
            self.ip_address.SetValue('127.0.0.1')
            return
        f = open('settings_c.txt', 'w')
        f.write(str(self.color_select_s.GetColour()[0]) + '\n')
        f.write(str(self.color_select_s.GetColour()[1]) + '\n')
        f.write(str(self.color_select_s.GetColour()[2]) + '\n')
        f.close()
        threading.Thread(name='main_client', target=Client.main, kwargs=dict(ip=self.ip_address.GetValue())).start()
        self.Close()
        self.Destroy()

    def webcam_fn(self, event):
 #       self.start.Disable()
        web_cam.window()
#        self.start.Enable()

    def __del__(self):
        wx.GetApp().ExitMainLoop()


def start():
    app = wx.App()
    e = Options(None, title='Size')
    app.MainLoop()