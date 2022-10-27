"""
Simulate the UDS Protocol using the Scapy Framework
"""

from scapy.all import *
from scapy.layers.can import *
from ecus.Engine import Engine
from scapy.contrib.automotive.uds import *
from scapy.contrib.automotive.ecu import *
from scapy.contrib.cansocket import CANSocket
from scapy.contrib.isotp import ISOTPSocket
import threading
import logging

load_layer("can")
load_contrib('cansocket')
load_contrib('isotp')
conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': False}
conf.contribs['CANSocket'] = {'use-python-can': False}


class Simulator:
    def __init__(self):
        # Initialize ECU(s)
        sock = ISOTPSocket("vcan0", sid=0x700, did=0x600, basecls=UDS)
        Engine().start(sock)

