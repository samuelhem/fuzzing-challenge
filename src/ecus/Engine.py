"""
Simulate Engine ECU Response Codes for Scapy Framework
"""
from scapy.all import *
from scapy.contrib.automotive.ecu import *
from scapy.contrib.automotive.uds import UDS, UDS_RC, UDS_RDBIPR, UDS_RCPR

import json
import threading
import logging
from .RoutineControl import Function, RC_SERVICE_PACKET


def load_routine_control_functions_from_file():
    logging.warning('Loading RC Functions for ECU...')
    try:
        file = open('./ecus/configs/routine_control_functions.json')
        return json.load(file)['functions']
    except FileNotFoundError:
        logging.warning('Could not open response config for Engine')


class Engine:
    functions = []

    def __init__(self):
        logging.warning('Initializing Engine ECU...')
        self.init_routine_control()

    def init_routine_control(self):
        functions = load_routine_control_functions_from_file()
        for f in functions:
            self.functions.append(Function(f['name'], f['identifier']))
        logging.warning('Done Loading Functions')

    def configure_routine_control_responses(self):
        ecu_responses = []
        for f in self.functions:
            ecu_responses.append(
                EcuResponse(EcuState(session=1),
                            responses=UDS(service=0x71) / UDS_RCPR(routineControlType=0x01,
                                                                   routineIdentifier=int(f.identifier, 0))
                                      / RC_SERVICE_PACKET(), answers=f.execute))
            ecu_responses.append(
                EcuResponse(EcuState(session=1),
                            responses=UDS(service=0x71) / UDS_RCPR(routineControlType=0x02,
                                                                   routineIdentifier=int(f.identifier, 0))
                                      / RC_SERVICE_PACKET(), answers=f.execute))

            ecu_responses.append(
                EcuResponse(EcuState(session=1),
                            responses=UDS(service=0x71) / UDS_RCPR(routineControlType=0x03,
                                                                   routineIdentifier=int(f.identifier, 0))
                                      / RC_SERVICE_PACKET(), answers=f.execute))
        return ecu_responses

    def start(self, socket):
        logging.warning('Starting Engine ECU...')
        configured_responses = self.configure_routine_control_responses()
        thread = threading.Thread(target=EcuAnsweringMachine(supported_responses=configured_responses,
                                                             main_socket=socket,
                                                             basecls=UDS,
                                                             timeout=None)).start()
        logging.warning('ECU started, thread running')
        return thread
