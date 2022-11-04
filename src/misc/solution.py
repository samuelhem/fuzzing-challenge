from scapy.all import *
from scapy.layers.can import *
from scapy.contrib.cansocket import CANSocket
from scapy.contrib.isotp import *
import threading
from scapy.contrib.automotive.uds import *
from time import sleep
conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': True}
conf.contribs['CANSocket'] = {'use-python-can': False}

load_contrib('isotp')
load_contrib('cansocket')
load_contrib('automotive.uds')
load_contrib('automotive.ecu')

sock = CANSocket('vcan0')
isotp = ISOTPSocket(sock, sid=0x600, did=0x700, basecls=UDS)


print(isotp.sr1(UDS()/UDS_RC(routineControlType=0x1, routineIdentifier=0x05), timeout=0.5, verbose=False))
print(isotp.sr1(UDS()/UDS_RC(routineControlType=0x1, routineIdentifier=0x07), timeout=0.5, verbose=False))
print(isotp.sr1(UDS()/UDS_RC(routineControlType=0x1, routineIdentifier=0x09), timeout=0.5, verbose=False))

sleep(5)

print(isotp.sr1(UDS()/UDS_RC(routineControlType=0x2, routineIdentifier=0x05), timeout=0.5, verbose=False))
print(isotp.sr1(UDS()/UDS_RC(routineControlType=0x2, routineIdentifier=0x05), timeout=0.5, verbose=False))

