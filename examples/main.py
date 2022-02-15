import sys
from gfConical.grainfather import Grainfather

username = ''    # Your username
password = ''    # Your password

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        username = args[0]
        password = args[1]

    gfIO = Grainfather(username, password)
    for conical in gfIO.conicals:
        print(f"{conical.name} is at {conical.temperature} with setpoint {conical.target_temperature}")
