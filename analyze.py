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
            'NormalvectorOut': dict(io='out'),

        }
        self._bufferX = np.array([])
        self._bufferZ = np.array([])
        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        size = int(self.ctrls['size'].value())
        self._bufferX = np.append(self._bufferX, kwds['XdataIn'])
        self._bufferX = self._bufferX[-size:]
        self._bufferZ = np.append(self._bufferZ, kwds['ZdataIn'])
        self._bufferZ = self._bufferZ[-size:]
        #output muss dann der ausgerechnete Normalvektor sein
        output = self._buffer
        print(self._buffer)
        return {'NormalvectorOut': output}

fclib.registerNodeType(NormalVectorNode, [('Data',)])






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

    pw1Node.setPlot(pw1



    pw2 = pg.PlotWidget()
    layout.addWidget(pw2, 0, 1)
    pw2.setYRange(0, 1024)

    pw2Node = fc.createNode('PlotWidget', pos=(350, 0))
    pw2Node.setPlot(pw2)

    pw3 = pg.PlotWidget()
    layout.addWidget(pw3, 0, 1)
    pw3.setYRange(0, 1024)

    pw3Node = fc.createNode('PlotWidget', pos=(350, 150))
    pw3Node.setPlot(pw3)


    pwNormalve = pg.PlotWidget()
    layout.addWidget(pw3, 0, 1)
    pw3.setYRange(0, 1024)

    pw3Node = fc.createNode('PlotWidget', pos=(350, 150))
    pw3Node.setPlot(pw3)


    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0),)
    buffer1Node = fc.createNode('Buffer', pos=(150, -150))
    buffer2Node = fc.createNode('Buffer', pos=(150, 0))
    buffer3Node = fc.createNode('Buffer', pos=(150, 150))
    normalVectorNode = fc.createNode('NormalVector', pos=(150, 300))

    fc.connectTerminals(wiimoteNode['accelX'], buffer1Node['dataIn'])
    fc.connectTerminals(wiimoteNode['accelY'], buffer2Node['dataIn'])
    fc.connectTerminals(wiimoteNode['accelZ'], buffer3Node['dataIn'])
    fc.connectTerminals(buffer1Node['dataOut'], pw1Node['In'])
    fc.connectTerminals(buffer2Node['dataOut'], pw2Node['In'])
    fc.connectTerminals(buffer3Node['dataOut'], pw3Node['In'])
    fc.connectTerminals(buffer1Node['dataOut'], normalVectorNode['XdataIn'])
    fc.connectTerminals(buffer3Node['dataOut'], normalVectorNode['ZdataIn'])

    print(buffer1Node['dataOut'])
  #  print(wiimote_node.BufferNode.process(buffer1Node))
    #CreateBufferNodeUFFERX")

    win.show()

    print(BufferNode.outputValues(buffer1Node))
    print(pw1.getPlotItem().dataItems)
    print(wiimote_node.WiimoteNode.outputValues(wiimoteNode))
   # print(BufferNode.)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
     #   print(BufferNode.outputValues(buffer1Node))
     #   print(pw1.getPlotItem().dataItems)
  #  if (sys.flags.interactive == 1) or  hasattr(QtCore, 'PYQT_VERSION'):
     #   QtGui.QApplication.instance().exec_()
     #   print(BufferNode.outputValues(buffer1Node))
      #  print(pw1.getPlotItem().dataItems)
