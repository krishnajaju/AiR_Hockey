import cv2
import numpy as np

# experiment with wxPython's wx.Slider
# wx.Slider(parent, id, init_val, min_val, max_val, position_tuple, size_tuple, style)
# position_tuple (x, y) of upper left corner, size_tuple (width, height)
# (on my Windows XP the mouse-wheel controls the slider that has the focus)
# tested with Python24 and wxPython26     vegaseat     17oct2005
import wx
import threading
from ConfigParser import SafeConfigParser

lower = np.array([10, 150, 100])
upper = np.array([30, 255, 255])
flag = True
def start():
    global lower, upper, flag
    cap = cv2.VideoCapture(0)
    while flag:
        _, frame = cap.read()
        #hue saturation value
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        kernal = np.ones((15, 15), np.float32)/225
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
        cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 255), -1)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.release()


class MyPanel(wx.Panel):
    def __init__(self, parent, id):
        global upper, lower
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")
        try:
            config = SafeConfigParser()
            config.read('HSV_Config.ini')
            l1 = int(config.get('Lower Bound', 'H'))
            l2 = int(config.get('Lower Bound', 'S'))
            l3 = int(config.get('Lower Bound', 'V'))
            u1 = int(config.get('Upper Bound', 'H'))
            u2 = int(config.get('Upper Bound', 'S'))
            u3 = int(config.get('Upper Bound', 'V'))
        except:
            l1 = l2 = l3 = u1 = u2 = u3 = 50
        self.lower_l = wx.StaticText(self, -1, label="Lower range", pos=(130, 20), name='lower')

        self.lower_h = wx.StaticText(self, -1, label="H", pos=(330, 90), name='H')
        self.slider1 = wx.Slider(self, -1, l1, 0, 255, (10, 80), (300, 50), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)

        self.lower_ = wx.StaticText(self, -1, label="S", pos=(330, 140), name='H')
        self.slider2 = wx.Slider(self, -1, l2, 0, 255, (10, 130), (300, 50), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)

        self.lower_v = wx.StaticText(self, -1, label="V", pos=(330, 190), name='S')
        self.slider3 = wx.Slider(self, -1, l3, 0, 255, (10, 180), (300, 50), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)

        self.upper_l = wx.StaticText(self, -1, label="Upper range", pos=(120, 250), name='upper')

        self.upper_l = wx.StaticText(self, -1, label="H", pos=(330, 290), name='H')
        self.slider4 = wx.Slider(self, -1, u1, 0, 255, (10, 280), (300, 50), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)

        self.upper_l = wx.StaticText(self, -1, label="S", pos=(330, 340), name='S')
        self.slider5 = wx.Slider(self, -1, u2, 0, 255, (10, 330), (300, 50), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)

        self.upper_l = wx.StaticText(self, -1, label="V", pos=(330, 390), name='V')
        self.slider6 = wx.Slider(self, -1, u3, 0, 255, (10, 380), (300, 50), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        lower = np.array([int(self.slider1.GetValue()), int(self.slider2.GetValue()), int(self.slider3.GetValue())])
        upper = np.array([int(self.slider4.GetValue()), int(self.slider5.GetValue()), int(self.slider6.GetValue())])
        self.save = wx.Button(self, id=wx.ID_ANY, label="Save", pos=(260, 430))
        self.Bind(wx.EVT_BUTTON, self.save_config, self.save)
        # respond to changes in slider position ...
        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)

    def sliderUpdate(self, event):
        global lower, upper
        lower = np.array([int(self.slider1.GetValue()), int(self.slider2.GetValue()), int(self.slider3.GetValue())])
        upper = np.array([int(self.slider4.GetValue()), int(self.slider5.GetValue()), int(self.slider6.GetValue())])

    def __del__(self):
        global flag
        self.Close()
        flag = False
    #     wx.GetApp().ExitMainLoop()

    def save_config(self, event):
        try:
            config = SafeConfigParser()
            config.add_section('Lower Bound')
            config.set('Lower Bound', 'H', str(self.slider1.GetValue()))
            config.set('Lower Bound', 'S', str(self.slider2.GetValue()))
            config.set('Lower Bound', 'V', str(self.slider3.GetValue()))
            config.add_section('Upper Bound')
            config.set('Upper Bound', 'H', str(self.slider4.GetValue()))
            config.set('Upper Bound', 'S', str(self.slider5.GetValue()))
            config.set('Upper Bound', 'V', str(self.slider6.GetValue()))
            f = open('HSV_Config.ini', 'w')
            config.write(f)
            f.close()
        except Exception as e:
            print(e)

def window():
    global flag
    flag = True
    app = wx.App(False)
    frame = wx.Frame(None, -1, "HSV", size=(380, 500))
    MyPanel(frame, -1)
    frame.Show(True)
    threading.Thread(name='cap', target=start).start()
    app.MainLoop()
