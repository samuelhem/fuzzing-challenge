"""
Simulate Engine ECU Response Codes for Scapy Framework
"""
from scapy.contrib.automotive.ecu import *
from scapy.contrib.automotive.uds import UDS, UDS_RC
import json
import threading
import logging


class Engine:
    responses = []

    def __init__(self):
        logging.warning('Initializing Engine ECU...')
        self.responses = self.load_ecu_responses_from_file()

    def load_ecu_responses_from_file(self):
        logging.warning('Loading ECU Response Configs...')
        try:
            file = open('./ecus/configs/engine_response_config.json')
            logging.warning('..Done Loading')
            return json.load(file)['responses']
        except FileNotFoundError:
            logging.warning('Could not open response config for Engine')

    def configure_responses(self, responses=None):
        config = responses[0]
        return [EcuResponse(EcuState(session=0x1, security_level=range(0, 255)),
                            responses=UDS() / UDS_RC(routineControlType=0x1, routineIdentifier=0x3))]

    def start(self, socket):
        logging.warning('Starting Engine ECU...')
        configured_responses = self.configure_responses(self.responses)
        thread = threading.Thread(target=EcuAnsweringMachine(supported_responses=configured_responses,
                                                             main_socket=socket,
                                                             basecls=UDS,
                                                             timeout=None)).start()
        logging.warning('ECU started, thread running')
        return thread
