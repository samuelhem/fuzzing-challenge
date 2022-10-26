"""
Simulate Engine ECU Response Codes for Scapy Framework
"""
from scapy.contrib.automotive.ecu import *
from scapy.contrib.automotive.uds import UDS
import json
import threading
import logging


class Engine:
    responses = []

    def __init__(self):
        logging.info('Initializing Engine ECU...')
        self.responses = self.load_ecu_responses_from_file()

    def load_ecu_responses_from_file(self):
        logging.info('Loading ECU Response Configs...')
        try:
            file = open('./ecus/configs/engine_response_config.json')
            logging.info('..Done Loading')
            return json.load(file)['responses']
        except FileNotFoundError:
            logging.error('Could not open response config for Engine')


    def configure_responses(self, responses=None):
        config = responses[0]
        return [EcuResponse(EcuState(session=config['sessionId'], security_level=config['securityLevel']),
                            responses=config['response'])]

    def start(self, socket):
        logging.info('Starting Engine ECU...')
        configured_responses = self.configure_responses(self.responses)
        thread = threading.Thread(target=EcuAnsweringMachine(supported_responses=configured_responses, main_socket=socket,
                                                    basecls=UDS,
                                                    timeout=None)).start()
        logging.info('ECU started, thread running')
        return thread
