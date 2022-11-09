from scapy.packet import Packet
from scapy.contrib.automotive.uds import *

from .States import States
from .DiagnosticSimulator import *
from .configs import config


# https://www.youtube.com/watch?v=z66WR7mfTMY
def is_state(function, stateToBe):
    if function.state == stateToBe:
        return True
    return False


def checkForSecurityState(request_packet):
    # early exit if security function is called
    if request_packet.routineIdentifier == config.SECURITY_ACCESS_ID:
        return True
    security_access_func = None
    # check if security function on id 0xFF3D is running
    for f in functionList:
        if f.identifier == hex(config.SECURITY_ACCESS_ID):
            security_access_func = f
    if security_access_func.state == States.RUNNING:
        return True
    else:
        return False


functionList = []


class Function:
    identifier = 0x00
    name = ""
    state = States.FINISHED
    runtime = 0
    time_remaining = 0

    def __init__(self, name, identifier, state=None):
        self.name = name
        self.identifier = identifier
        if state is not None:
            self.state = state

    def start(self):
        if is_state(self, States.FINSIHED_WITH_ERROR):
            return " Function that has Failed cannot run again"
        if not is_state(self, States.RUNNING):
            return start_simulation(self)

    def stop(self):
        if is_state(self, States.RUNNING):
            self.state = States.STOPPED
        else:
            return " Function that is not Running cannot be stopped"

    def status(self):
        if self.state == States.RUNNING:
            return " {}: {} time remaining: {}".format(self.name, self.state.name, self.time_remaining)
        return " {}: {}".format(self.name, self.state.name)

    def execute(self, resp, req):
        # Check for SecurityAccess
        if resp.routineIdentifier == req.routineIdentifier \
                and resp.routineControlType == req.routineControlType:
            if not checkForSecurityState(req):
                print("NO ACCESS")
                return False
            else:
                if req.routineControlType == 1:
                    resp.message = self.start()
                elif req.routineControlType == 2:
                    resp.message = self.stop()
                elif req.routineControlType == 3:
                    resp.message = self.status()
                else:
                    return False
                resp.state = self.state.value
                print(self.state.value)
                return resp.answers(req)
        else:
            return False


class RC_SERVICE_PACKET(Packet):
    name = 'Routine_Control_Service_Packet'
    fields_desc = [
        ShortField('state', 0),
        StrField('message', 0),
    ]

# bind_layers(UDS_RCPR, RC_SERVICE_PACKET, routineIdentifier=)
# UDS_RC.routineControlIdentifiers[0x05] = 'StatusPaket'
