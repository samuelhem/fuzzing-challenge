"""
Simulate Engine ECU Response Codes for Scapy Framework
"""
from scapy.contrib.automotive.ecu import *
from scapy.contrib.automotive.uds import UDS, UDS_RCPR

import json
import threading
import logging
from src.ecu.services.RoutineControl import Function, RC_SERVICE_PACKET, functionList
from src.ecu.services.Services import serviceResponses


def load_json_file(file_path):
    try:
        file = open(file_path)
        return json.load(file)
    except FileNotFoundError:
        logging.error('Could not open {}'.format(file_path))


def load_routine_control_functions_from_file():
    routine_control_functions = load_json_file(
        '/tmp/pycharm_project_854/src/ecu/configs/routine_control_functions.json')
    return routine_control_functions['functions']


def load_other_uds_functions_from_file():
    uds_functions = load_json_file('/tmp/pycharm_project_854/src/ecu/configs/services.json')
    return uds_functions['services']


class Engine:

    def __init__(self):
        logging.warning('Initializing Engine ECU...')
        self.init_routine_control()
       # self.init_services()

    def init_routine_control(self):
        functions = load_routine_control_functions_from_file()
        for f in functions:
            functionList.append(Function(f['name'], f['identifier']))
        logging.warning('Done Loading Functions')

    def init_services(self):
        functions = load_other_uds_functions_from_file()
        for f in functions:
            # TODO: implement services
            return
        logging.warning('Done Loading Services')

    def configure_routine_control_responses(self):
        rc_responses = []
        for f in functionList:
            rc_responses.append(
                EcuResponse(EcuState(session=1),
                            responses=UDS(service=0x71) / UDS_RCPR(routineControlType=0x01,
                                                                   routineIdentifier=int(f.identifier, 0))
                                      / RC_SERVICE_PACKET(), answers=f.execute))
            rc_responses.append(
                EcuResponse(EcuState(session=1),
                            responses=UDS(service=0x71) / UDS_RCPR(routineControlType=0x02,
                                                                   routineIdentifier=int(f.identifier, 0))
                                      / RC_SERVICE_PACKET(), answers=f.execute))

            rc_responses.append(
                EcuResponse(EcuState(session=1),
                            responses=UDS(service=0x71) / UDS_RCPR(routineControlType=0x03,
                                                                   routineIdentifier=int(f.identifier, 0))
                                      / RC_SERVICE_PACKET(), answers=f.execute))
        return rc_responses

    def configure_basic_responses_for_uds(self):
        uds_service_responses = []
        return uds_service_responses

    def start(self, socket):
        logging.warning('Starting Engine ECU...')
        configured_responses = [*self.configure_routine_control_responses(), *self.configure_basic_responses_for_uds()]
        thread = threading.Thread(target=EcuAnsweringMachine(supported_responses=configured_responses,
                                                             main_socket=socket,
                                                             basecls=UDS,
                                                             timeout=None)).start()
        logging.warning('ECU started, thread running')
        return thread
