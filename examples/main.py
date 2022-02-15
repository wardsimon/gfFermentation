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
    conicals = gfIO.get_conicals()
    for conical in conicals:
        print(conical.temperature)
