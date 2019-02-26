# -*- coding: utf-8 -*-
# @Time     :2019/2/25
# @Author   :qpf

from threading import Thread
import wx

data = ''


class SpeechGui(wx.Frame):
    def __init__(self, parent, q):
        self.title = '语音识别检测'
        wx.Frame.__init__(self, parent, id=-1, title=self.title,
                          size=(300, 200))
        self.panel = wx.Panel(self)
        self.box = wx.BoxSizer(wx.VERTICAL)

        self.center = wx.TextCtrl(self.panel, -1, size=(280, 180), style=wx.TE_READONLY | wx.TE_MULTILINE)

        font = wx.Font(pointSize=18, family=wx.FONTFAMILY_DECORATIVE, style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_NORMAL)
        self.center.SetFont(font)

        self.box.Add(self.center, 0, wx.ALIGN_CENTER)
        self.panel.SetSizer(self.box)

        Thread(target=recv, args=(self.center, q,)).start()


def main(q=None):
    app = wx.PySimpleApp()
    frame = SpeechGui(None, q=q)
    frame.Show()
    app.MainLoop()


def recv(obj, q=None):
    global data
    cache = ''
    while True:
        if q is not None:
            if q.empty() is not True:
                data = q.get()
                print('接收队列数据：', data)
                # 每行显示9个字
                for i in range(0, len(data), 9):
                    str_split = data[i:i + 9]
                    str = str_split + '\n'
                    cache = cache + str
                obj.AppendText(cache)
                cache = ''
        else:
            data = '呵呵哈哈哈哈哈或'
            obj.AppendText(data)


if __name__ == '__main__':
    main()
