#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
Get data from Magnescale LT30
{License_info}
"""
__filename__ = 'lt30_gui.py'
__author__ = 'Andre Wiegleb'
__created__ = '02.04.2024'
__copyright__ = 'Copyright 2023, MAgnescale LT30'
__license__ = 'GPL'
__version__ = '0.1.0'
__maintainer__ = 'Andre Wiegleb'
__email__ = 'andre.wiegleb@mts.com'
__status__ = 'production'

import sys
import time
import threading
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# import the LT30 class from lib.lt30
from lib.lt30 import LT30

lt30 = LT30('COM3')


def thread_function():
    """ Function to be executed in a thread"""
    global running, value
    while running:
        try:
            offset = float(input_field.text() or 0)
        except Exception as e:
            offset = 0
            print(e)
        try:
            ref_value = float(lt30.read())
            value = ref_value + offset
            update_display(round(value, 3))
            time.sleep(0.1)
        except Exception as e:
            print(e)


def update_display(value):
    """ Update the display with the given value"""
    label.setText(f" {value}")


# Starte den Thread
def start_thread():
    """ Start the thread to read values from LT30"""
    global running
    running = True
    thread = threading.Thread(target=thread_function)
    thread.start()


def stop_thread():
    """ Stop the thread"""
    global running
    running = False


def restart():
    """ Restart/reset the display"""
    stop_thread()
    lt30.tare()
    print('Tare')
    time.sleep(0.2)
    start_thread()


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("LT30 Display")

layout = QVBoxLayout()

font = QFont('Arial', 60, QFont.Bold)
label = QLabel("LT30")
label.setFont(font)
label.setAlignment(Qt.AlignRight)
layout.addWidget(label)

input_field = QLineEdit()
input_field.setPlaceholderText("Offset")
layout.addWidget(input_field)

start_button = QPushButton("Start")
start_button.clicked.connect(start_thread)
layout.addWidget(start_button)

stop_button = QPushButton("Stop")
stop_button.clicked.connect(stop_thread)
layout.addWidget(stop_button)

reset_button = QPushButton("Reset")
reset_button.clicked.connect(restart)
layout.addWidget(reset_button)

window.setLayout(layout)
window.show()

running = False
value = 0

sys.exit(app.exec_())
