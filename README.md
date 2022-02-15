# gfConical - Control the Grainfather Conical fermenter.

This simple package allows for reading the temperature/set point of a Grainfather Conical fermenter and setting of target temperature/pausing. 

## Install
gfConical is available on pip
```
pip install gfconical
```


## Usage
```
from gfConical import Grainfather

username = ''    # Your username
password = ''    # Your password

gfIO = Grainfather(username, password)
for conical in gfIO.conicals:
    print(f"{conical.name} is at {conical.temperature} with setpoint {conical.target_temperature}")
 ```
