# gfConical

Python control of the Grainfather Conical fermenter

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
conicals = gfIO.getConicals()
for conical in conicals:
    print(conical.temperature)
 ```
