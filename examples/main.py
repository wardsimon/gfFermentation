import sys
from gfFermentation.grainfather import Grainfather

username = ''    # Your username
password = ''    # Your password

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        username = args[0]
        password = args[1]

    gfIO = Grainfather(username, password)
    for controller in gfIO.controllers:
        if controller.online:
            print(f"{controller.name} is at {controller.temperature} with setpoint {controller.target_temperature}")
