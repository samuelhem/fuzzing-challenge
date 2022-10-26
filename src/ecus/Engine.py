"""
Simulate Engine ECU Response Codes for Scapy Framework
"""
from scapy.contrib.automotive.ecu import *
from scapy.contrib.automotive.uds import UDS
import json


class Engine:
    responses = []

    def __init__(self):
        self.responses = self.load_ecu_responses_from_file()

    def load_ecu_responses_from_file(self):
        file = open('./ecus/configs/engine_response_config.json')
        return json.load(file)['responses']

    def configure_responses(self, responses=None):
        config = responses[0]
        return [EcuResponse(EcuState(session=config['sessionId'], security_level=config['securityLevel']),
                            responses=config['response'])]

    def start(self, socket):
        configured_responses = self.configure_responses(self.responses)
        return EcuAnsweringMachine(supported_responses=configured_responses, main_socket=socket, basecls=UDS,
                                   timeout=None)
