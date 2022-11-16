from scapy.packet import Packet
from scapy.contrib.automotive.uds import *

from src.ecu.States import States
from src.ecu.DiagnosticSimulator import *
from src.ecu.configs import config
import src.ecu.Util as Util
import src.ecu.Security as Security
from scapy.fields import RawVal


# https://www.youtube.com/watch?v=z66WR7mfTMY
def is_state(function, state_to_be):
    if function.state == state_to_be:
        return True
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
            # Return Random Key Value for Security Function on ID 309
            if req.routineIdentifier == config.SECURITY_KEY_ID:
                resp.state = 0x02
                resp.message = Util.int_to_hex_tuple(Security.createRandomKey())
                # return early
                return resp.answers(req)
            # Can only ever be a good request if the Key is present
            if hasattr(req, "load"):
                if not Security.checkKey(int.from_bytes(req.load, 'big')):
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
                    return resp.answers(req)
            else:
                print("No Access")
                return False
        else:
            return False


class RC_SERVICE_PACKET(Packet):
    name = 'Routine_Control_Service_Packet'
    fields_desc = [
        ShortField('state', 0),
        StrField('message', 0)
    ]

# bind_layers(UDS_RCPR, RC_SERVICE_PACKET, routineIdentifier=)
# UDS_RC.routineControlIdentifiers[0x05] = 'StatusPaket'
