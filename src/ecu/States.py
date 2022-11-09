from enum import Enum


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
