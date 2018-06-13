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
import math
import wiimote
import wiimote_node
import time
import sys
from wiimote_node import BufferNode


# Eigene Erstellte Klasse für den NormalenvektorNode
# Hier kommen die Daten von den Buffernodes rein, die ja die richtigen Daten der Fernbedienung sind
# und dann müssen wir noch die Normale berechnen
class NormalVectorNode(CtrlNode):

    nodeName = "NormalVector"
    uiTemplate = [
        ('size',  'spin', {'value': 32.0, 'step': 1.0, 'bounds': [0.0, 128.0]}),
    ]

    def __init__(self, name):
        terminals = {
            'XdataIn': dict(io='in'),
            'ZdataIn': dict(io='in'),
            'dataOut': dict(io='out'),

        }
        self._bufferX = np.array([])
        self._bufferZ = np.array([])
        self.list = []
        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        size = int(self.ctrls['size'].value())
        self._bufferX = np.append(self._bufferX, kwds['XdataIn'])
        self._bufferX = self._bufferX[-size:]
        self._bufferZ = np.append(self._bufferZ, kwds['ZdataIn'])
        self._bufferZ = self._bufferZ[-size:]
        output = self.normalVector()
        return {'dataOut': output}

    def normalVector(self):
        for i in range(len(self._bufferX)):
            x = - self._bufferZ[i]
            y = self._bufferX[i]
            normalvectorlocal = (x, y)
            squareroot = math.sqrt(x*x + y*y)
            unitnormalvectorx = normalvectorlocal[0] / squareroot
            unitnormalvectory = normalvectorlocal[1] / squareroot
            self.list= ((0, 0), (unitnormalvectorx, unitnormalvectory))
            return self.list

fclib.registerNodeType(NormalVectorNode, [('Data',)])

class PlotCurveNode(CtrlNode):

    nodeName = "PlotCurveNode"
    uiTemplate = [
        ('size',  'spin', {'value': 32.0, 'step': 1.0, 'bounds': [0.0, 128.0]}),
    ]

    def __init__(self, name):
        terminals = {
            'dataIn': dict(io='in'),
            'plot': dict(io='out'),

        }
        self.input = np.array([])
        self.output = np.array([])
        CtrlNode.__init__(self, name, terminals=terminals)

    def getVector(self):
        self.output = self.input

    def process(self, **kwds):
        size = int(self.ctrls['size'].value())
        self.input = np.append(self.input, kwds['dataIn'])
        self.getVector()
        return {'plot': self.output}

fclib.registerNodeType(PlotCurveNode, [('Data',)])

if __name__ == '__main__':
#    NormalVectorNode(CtrlNode)
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


    pw1Node = fc.createNode('PlotWidget', pos=(350, -150))

    pw1Node.setPlot(pw1)



    pw2 = pg.PlotWidget()
    layout.addWidget(pw2, 0, 2)
    pw2.setYRange(0, 1024)

    pw2Node = fc.createNode('PlotWidget', pos=(350, 0))
    pw2Node.setPlot(pw2)

    pw3 = pg.PlotWidget()
    layout.addWidget(pw3, 1, 1)
    pw3.setYRange(0, 1024)

    pw3Node = fc.createNode('PlotWidget', pos=(350, 150))
    pw3Node.setPlot(pw3)


    pwNormalve = pg.PlotWidget()
    layout.addWidget(pwNormalve, 1, 2)
    pwNormalve.setYRange(-1, 1)

    pwNormalveNode = fc.createNode('PlotWidget', pos=(300, 150))
    pwNormalveNode.setPlot(pwNormalve)


    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0),)
    buffer1Node = fc.createNode('Buffer', pos=(150, -150))
    buffer2Node = fc.createNode('Buffer', pos=(150, 0))
    buffer3Node = fc.createNode('Buffer', pos=(150, 150))
    normalVectorNode = fc.createNode('NormalVector', pos=(150, 300))
    plotCurve = fc.createNode('PlotCurveNode', pos=(200, 100))

    fc.connectTerminals(wiimoteNode['accelX'], buffer1Node['dataIn'])
    fc.connectTerminals(wiimoteNode['accelY'], buffer2Node['dataIn'])
    fc.connectTerminals(wiimoteNode['accelZ'], buffer3Node['dataIn'])
    fc.connectTerminals(buffer1Node['dataOut'], pw1Node['In'])
    fc.connectTerminals(buffer2Node['dataOut'], pw2Node['In'])
    fc.connectTerminals(buffer3Node['dataOut'], pw3Node['In'])
    fc.connectTerminals(buffer1Node['dataOut'], normalVectorNode['XdataIn'])
    fc.connectTerminals(buffer3Node['dataOut'], normalVectorNode['ZdataIn'])
    fc.connectTerminals(normalVectorNode['dataOut'], plotCurve['dataIn'])
    fc.connectTerminals(plotCurve['plot'], pwNormalveNode['In'])

    win.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
