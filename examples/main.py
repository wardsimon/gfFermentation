from gfConical.grainfather import Grainfather

username = ''    # Your username
password = ''    # Your password

if __name__ == "__main__":
    gfIO = Grainfather(username, password)
    conicals = gfIO.getConicals()
    for conical in conicals:
        print(conical.temperature)
