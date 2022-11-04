from .States import States
from threading import *
from random import randint, randrange
from time import sleep


def simulation(arg):
    # Basic Simulation
    print("Simulation now Running")
    arg.state = States.RUNNING
    x = 0
    # Constantly Check for State Changes to Stop the Simulation
    while True:
        if arg.state == States.STOPPED:
            print("Sim is stopped")
            return
        sleep(1)
        x += 1

    if randrange(10) == 0:  # 10% Chance to Finish with Error
        print("Sim is Error")
        arg.state = States.FINSIHED_WITH_ERROR
    else:
        print("Sim is Done")
        arg.state = States.FINISHED


def start_simulation(function):
    thread = Thread(target=simulation, args=(function,))
    thread.start()
