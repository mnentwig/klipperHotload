# KlipperHotload
Convenient use of Python in Klipper GCODE with runtime recompile

### Motivation
Writing user Python modules for Klipper tends to be clumsy, as any change requires restarting Klipper with rehoming etc.

### Enter KlipperHotload
The package provides a single Klipper macro ```U``` that executes user Python code, re-compiling source code if changed.

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
calls the last user function, file, path that were specified. Defaults are `my_fun` in `my_fun.py`, located in the same directory as `printer.cfg`. 
This variant is attractive for quick-and-dirty use, also when only a single function exists (e.g. user code command dispatcher)

Arguments are passed through e.g.:
```gcode
U FOOBAR=10
```
Reserved keywords: ```PATH```, ```FILE```, ```FUN```, ```CLEAR``` 

```U FUN=other_fun```
calls `other_fun` and sets it as default.

```U FUN=fun3 FILE=someOtherFile.py PATH=/home/myself```
calls `fun3` from `someOtherFile.py` located at `/home/myself` and updates defaults for `PATH`, `FILE`, `FUN`.

### Installation
- run klipperHotload/install.sh
- add [klipper_hotload] to e.g. printer.cfg
- Run `U` from the Klipper command line. The error message shows the default file location. Copy above example there into my_fun.py.

# Reference

### PATH and FILE resolution
`FILE` may optionally include an absolute or relative file component. It updates the default for `FILE` (not `PATH`). If absolute, `PATH` is disregarded. 
A typical use case is setting `PATH` only once to a user folder, then relying on the `PATH` default and navigating subfolders with `FILE=/a/b/c/d.py`. 
The intention behind the default mechanisms is to keep G-code concise in long lists of function calls that typically call functions from the same file or even the same function with changing arguments.

### PATH and FILE variables
`{HOME}` interpolates to the user's home directory, `CONFIG` to the directory holding printer.cfg, `{TEMP}` to the system temp directory, and `EXTRAS` to the install location of the python file (e.g. /home/someUser/klipper/klippy/extras)

### Storage
A single dictionary is provided to all function calls for data storage, regardless of file. It persists across recompilation of user code. Restarting Klipper clears it. 
User code is responsible for avoiding name clashes between functions e.g. by using uniquely named fields (see `myOwnData` field in example).

Storage can be reset with the ```CLEAR=1``` argument in combination with a function call, which also forces recompilation of the function's source file (clearing e.g. global variables in the file's name space)

The dictionary permits dot notation for dictionary access as shorthand.

### Running tests
Copy contents of `klipper/extras/klipper_hotload_demotest/demotest.gcode` into the Klipper console.