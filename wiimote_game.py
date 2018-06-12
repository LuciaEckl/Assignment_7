#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

import wiimote
import time
import sys
import webbrowser

"""
A simple demo script for the wiimote.py module.
Start as `python3 wiimote_demo.py [bluetooth address of Wiimote]` and follow
instructions.
"""

sys.stdout.write("Press the 'sync' button on the back of your Wiimote Plus \n" +
                 "Press <return> once the Wiimote's LEDs start blinking. \n")

gameOn = True
firstTask = False
secondTask = False
thirdTask = False


if len(sys.argv) == 1:
    addr, name = wiimote.find()[0]
elif len(sys.argv) == 2:
    addr = sys.argv[1]
    name = None
elif len(sys.argv) == 3:
    addr, name = sys.argv[1:3]
sys.stdout.write(("Connecting to %s (%s)" % (name, addr)))
wm = wiimote.connect(addr, name)


# When the wiimote is connecte the leds start to blink
patterns = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 0, 0]]
for i in range(5):
    for p in patterns:
        wm.leds = p
        time.sleep(0.05)


# By Katharina Lichtner
# The user should press the button which is displayed on the command line.
# after every task the next led on the wiimote starts to light
# at the last task the wiimote rumbles and a webpage is opened.
# source: https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python last access: 06.06.2018
while gameOn:
    sys.stdout.write("Press the displayed buttons to get points for your highscore \n")
    sys.stdout.write("\n Press the A Button \n")
    print("Statusfirsttast", firstTask)
    while True:
        homepage_link = "http://www.kamelrechner.eu/de"
        if (wm.buttons["A"] is True) and (firstTask is False):
            wm.leds[1] = True
            sum += 10
            firstTask = True
            print(firstTask, wm.buttons)
            sys.stdout.write("Press the B Button \n")

        if ((wm.buttons["B"] is True) and (firstTask is True) and (secondTask is False)):
            sys.stdout.write("Press the A and B Button at the same time \n")

            wm.leds[2] = True
            sum += 10
            secondTask = True
        if ((wm.buttons["A"] is True) and (wm.buttons["B"] is True) and (firstTask is True)
                and (secondTask is True) and (thirdTask is False)):
            wm.leds[3] = True
            sum += 10
            thirdTask = True
        if firstTask is True and secondTask is True and thirdTask is True and gameOn is True:
            wm.rumble(0.5)
            sys.stdout.write("You won! Now a website will open! \n")
            webbrowser.open(homepage_link)
            gameOn = False
        else:
            pass
        time.sleep(0.05)
