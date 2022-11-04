from enum import Enum
from scapy.packet import Packet
from scapy.contrib.automotive.uds import *


# https://www.youtube.com/watch?v=z66WR7mfTMY

def check_state(function, stateToBe):
    if function.state == stateToBe:
        print("Function `{}` is already Running".format(function.name))
        return False
    function.state = stateToBe
    return "    Function `{}`: is now {}".format(function.name, stateToBe.name)

class States(Enum):
    UNDEFINED = 0x00
    RUNNING = 0x01
    FINISHED = 0x02
    FINSIHED_WITH_ERROR = 0x03
    STOPPED = 0x04

    @staticmethod
    def return_as_dict():
        return {
            0x00: 'UNDEFINED',
            0x01: 'RUNNING',
            0x02: 'FINISHED',
            0x03: 'FINISHED_WITH_ERROR',
            0x04: 'STOPPED'
        }


class Function:
    identifier = 0x00
    name = ""
    state = States.UNDEFINED

    def __init__(self, name, identifier, state=None):
        self.name = name
        self.identifier = identifier
        if state is not None:
            self.state = state

    def start(self):
        check_state(self, States.RUNNING)

    def stop(self):
        check_state(self, States.STOPPED)

    def status(self):
        return " {} currently {}".format(self.name, self.state.name)

    def execute(self, resp, req):
        if resp.routineIdentifier == req.routineIdentifier \
                and resp.routineControlType == req.routineControlType:
            if req.routineControlType == 1:
                self.start()
            elif req.routineControlType == 2:
                self.stop()
            elif req.routineControlType == 3:
                resp.message = self.status()
            else:
                return False
            resp.state = self.state.value
            return resp.answers(req)
        else:
            return False


class RC_SERVICE_PACKET(Packet):
    name = 'Routine_Control_Service_Packet'
    fields_desc = [
        ShortField('state', 0),
        StrField('message', 0)
    ]

#bind_layers(UDS_RCPR, RC_SERVICE_PACKET, routineIdentifier=)
#UDS_RC.routineControlIdentifiers[0x05] = 'StatusPaket'

