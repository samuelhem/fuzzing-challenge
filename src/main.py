# This is a sample Python script.


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from scapy.all import *
from scapy.layers.can import *
from ecus.Engine import Engine
from scapy.contrib.automotive.uds import *
from scapy.contrib.automotive.ecu import *
from scapy.contrib.cansocket import CANSocket
import threading

from scapy.contrib.isotp import ISOTPSocket

load_layer("can")

load_contrib('cansocket')
load_contrib('isotp')

conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': False}
conf.contribs['CANSocket'] = {'use-python-can': False}

def main():
    print(123)
    sock = ISOTPSocket("vcan0", sid=0x700, did=0x600, basecls=UDS)
    engine = Engine().start(sock)


if __name__ == '__main__':
    main()
