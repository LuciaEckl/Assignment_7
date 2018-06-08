#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

# this code is adapted to wiimote_node.py from Raphael Wimmer

from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

import wiimote

import wiimote_node

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('WiimoteNode demo')
    cw = QtGui.QWidget()
    win.setCentralWidget(cw)
    layout = QtGui.QGridLayout()
    cw.setLayout(layout)

    # Create an empty flowchart with a single input and output
    fc = Flowchart(terminals={
    })
    w = fc.widget()

    layout.addWidget(fc.widget(), 0, 0, 2, 1)

    pw1 = pg.PlotWidget()
    layout.addWidget(pw1, 0, 1)
    pw1.setYRange(0, 1024)

    pw1Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw1Node.setPlot(pw1)

    #print(pw1Node.update_all_sensors())

    pw2 = pg.PlotWidget()
    layout.addWidget(pw2, 0, 1)
    pw2.setYRange(0, 1024)

    pw2Node = fc.createNode('PlotWidget', pos=(0, 100))
    pw2Node.setPlot(pw2)

    pw3 = pg.PlotWidget()
    layout.addWidget(pw3, 0, 1)
    pw3.setYRange(0, 1024)

    pw3Node = fc.createNode('PlotWidget', pos=(0, 150))
    pw3Node.setPlot(pw3)


    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0), )
    buffer1Node = fc.createNode('Buffer', pos=(150, 0))
    buffer2Node = fc.createNode('Buffer', pos=(100, 50))
    buffer3Node = fc.createNode('Buffer', pos=(200, 50))

    fc.connectTerminals(wiimoteNode['accelX'], buffer1Node['dataIn'])
    fc.connectTerminals(wiimoteNode['accelY'], buffer2Node['dataIn'])
    fc.connectTerminals(wiimoteNode['accelZ'], buffer3Node['dataIn'])
    fc.connectTerminals(buffer1Node['dataOut'], pw1Node['In'])
    fc.connectTerminals(buffer2Node['dataOut'], pw2Node['In'])
    fc.connectTerminals(buffer3Node['dataOut'], pw3Node['In'])

    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()



