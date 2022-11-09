from .States import States
from threading import *
from random import randint, randrange
from time import sleep
from .configs import config


def simulation(arg):
    # Basic Simulation
    print("Simulation now Running")
    arg.state = States.RUNNING
    arg.runtime = randrange(0, 300)
    if arg.identifier == hex(config.SECURITY_ACCESS_ID):
        arg.runtime = 100000
        print("SECURITY ACCESS GRANTED")

    # Constantly Check for State Changes to Stop the Simulation
    arg.time_remaining = arg.runtime
    while arg.time_remaining > 0:
        if arg.state == States.STOPPED:
            print("Sim is stopped")
            return
        sleep(1)
        arg.time_remaining -= 1

    if randrange(10) == 0:  # 10% Chance to Finish with Error
        print("Sim is Error")
        arg.state = States.FINSIHED_WITH_ERROR
    else:
        print("Sim is Done")
        arg.state = States.FINISHED


def start_simulation(function):
    thread = Thread(target=simulation, args=(function,))
    thread.start()
