# -*- coding: utf-8 -*-
# @Time     :2019/2/25
# @Author   :qpf


from queue import Queue

import gui
import detect_voice

q = Queue()
m = detect_voice.Main()
m.main(q=q)
gui.main(q=q)
