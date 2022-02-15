# gfConical - Control the Grainfather Conical fermenter.

This simple package allows for reading the temperature/set point of a Grainfather Conical fermenter and setting of target temperature/pausing. 

## Install
gfConical is available on pip
```
pip install gfconnical
```


## Usage
```
from gfConical.grainfather import Grainfather

username = ''    # Your username
password = ''    # Your password

gfIO = Grainfather(username, password)
conicals = gfIO.get_conicals()
for conical in conicals:
    print(conical.temperature)
 ```
