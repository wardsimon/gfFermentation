# gfFermentation - Script Grainfather fermenter controlers.

This package allows for reading/controlling a Grainfather Conical fermenter or fermentation device. Currently reading and setting of target temperature/pausing and status is supported. 

## Install
gfFermentation is available on pip
```
pip install gffermentation
```


## Usage
```
from gfFermentation.grainfather import Grainfather

username = ''    # Your username
password = ''    # Your password

gfIO = Grainfather(username, password) # Login to Grainfather (tokens also supported)

for controller in gfIO.controllers:
    print(controller)
 ```
