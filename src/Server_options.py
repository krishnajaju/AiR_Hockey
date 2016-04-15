import wx
import socket
import Server
import threading
import image_detection as web_cam

class Options(wx.Frame):
    def __init__(self, parent, title):
        super(Options, self).__init__(parent, title=title, size=(400, 300))
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour("black")
        self.panel.SetForegroundColour("white")
        self.start = wx.Button(self.panel, id=wx.ID_ANY, label="Start", pos=(250, 200))
        self.Bind(wx.EVT_BUTTON, self.start_server_fn, self.start)
        self.webcam = wx.Button(self.panel, id=wx.ID_ANY, label="Test Webcam", pos=(250, 100))
        self.Bind(wx.EVT_BUTTON, self.webcam_fn, self.webcam)
        self.ip = wx.StaticText(self.panel, -1, label="IP address:" , pos=(10, 20), name='ip')

        self.ip_addr = wx.StaticText(self.panel, -1, label='%s' % socket.gethostbyname(socket.gethostname()), pos=(100, 15), name='ip addr')
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        self.ip_addr.SetFont(font)

        self.color_s_l = wx.StaticText(self.panel, -1, label="Server Color:", pos=(10, 55), name='color')
        self.color_select_s = wx.ColourPickerCtrl(self.panel, id=wx.ID_ANY, pos=(100, 55))
        self.color_select_s.SetColour((255, 0, 0))

        self.color_c_l = wx.StaticText(self.panel, -1, label="Puck Color:", pos=(10, 95), name='color')
        self.color_select_p = wx.ColourPickerCtrl(self.panel, id=wx.ID_ANY, pos=(100, 95))
        self.color_select_p.SetColour((0, 255, 0))

        self.time_l = wx.StaticText(self.panel, -1, label="Time:", pos=(10, 145), name='time')
        self.time = wx.TextCtrl( self.panel, -1, pos=(100,145))
        self.time.SetLabel('-1')

        self.score_l = wx.StaticText(self.panel, -1, label="Max Score:", pos=(10, 185), name='score')
        self.score = wx.TextCtrl(self.panel, -1, pos=(100,185))
        self.score.SetLabel('-1')

        self.SetTitle('Server')
        self.Centre()
        self.Show(True)

    def start_server_fn(self, event):
        f = open('settings_s.txt', 'w')
        f.write(self.time.GetValue() + '\n')
        f.write(self.score.GetValue() + '\n')
        f.write(str(self.color_select_s.GetColour()[0]) + '\n')
        f.write(str(self.color_select_s.GetColour()[1]) + '\n')
        f.write(str(self.color_select_s.GetColour()[2]) + '\n')

        f.write(str(self.color_select_p.GetColour()[0]) + '\n')
        f.write(str(self.color_select_p.GetColour()[1]) + '\n')
        f.write(str(self.color_select_p.GetColour()[2]) + '\n')
        f.close()
        threading.Thread(name='main', target=Server.main).start()
        self.Close()

    def webcam_fn(self, event):
        self.start.Disable()
        web_cam.start()
        self.start.Enable()

app = wx.App()
e = Options(None, title='Size')
app.MainLoop()