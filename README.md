# KlipperHotload
Convenient use of Python in Klipper GCODE with runtime recompile

### Motivation
Writing user Python modules for Klipper tends to be clumsy, as any change requires restarting Klipper with rehoming etc.

### Enter KlipperHotload
The package provides a single Klipper macro ```U``` that executes user Python code, hotloading as needed.

### User function example
```python
def my_fun(self, gcmd):
	# Accessible:
	# - self.printer
	# - self.log("the response is spam spam bacon eggs and spam")
	# - self.logE("respond this as error")
	# user data: Persistent until Klipper restart or explicit CLEAR=1
	# self.myOwnData is shorthand for self["myOwnData"]
	# Fields are visible to any other function call - use e.g. prefix to prevent name clash
    if not "myOwnData" in self:
        self.log("Startup - hello there!")
        self.myOwnData={"foobarCt":123} 
    mod = self.myOwnData
    # Example code on self.printer:
    FOOBAR = gcmd.get_int("FOOBAR", default=None)
    curtime = self.printer.get_reactor().monotonic()
    toolhead = self.printer.lookup_object('toolhead')
    homedAxes = toolhead.get_status(curtime)['homed_axes']
    if FOOBAR is not None:
        mod["foobarCt"] = FOOBAR
    else:
        mod["foobarCt"] = mod["foobarCt"]-1
    self.log("Remaining foobars: "+str(mod["foobarCt"])+". Homed axes are: "+str(homedAxes))

def otherFun(self, gcmd): # use FUN=otherFun
    self.log("via otherFun:")
	my_fun(self, gcmd)
```

### Usage
```gcode
U
```
uses the last user function, file, path that were specified. Defaults are `my_fun` in `my_fun.py`, located in the same directory as `printer.cfg`. 
This variant is attractive for quick-and-dirty use, also when only a single function exists (e.g. user code command dispatcher)

Arguments are passed through:
```gcode
U FOOBAR=10
```
Arguments are passed through. Reserved keywords: ```PATH```, ```FILE```, ```FUN```, ```CLEAR``` 


### Example (complete)
This GCODE
```U FUN=my_other_fun FILE=my_other_file PATH=```
executes `my_fun` in `my_fun.py`, assumed to be in the same directory as `printer.cfg`.

### PATH and FILE variables
`{HOME}` interpolates to the user's home directory, `CONFIG` to the directory holding printer.cfg, `{TEMP}` to the system temp directory, 



### Storage



### Installation
- run klipperHotload/install.sh
- add [klipper_hotload] to e.g. printer.cfg