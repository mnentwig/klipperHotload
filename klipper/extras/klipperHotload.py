import os
from pathlib import Path
import tempfile

class klipperHotload:
    # dictionary that uses dot for element access
    class attrDict(dict):
        def __getattr__(self, name):
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)
        def __setattr__(self, name, value):
            self[name] = value

    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.myFunDict = None # first argument given to user code calls
        self.codeNamespace = {} # user file compilation result, indexed by canonical path
        self.codeTimestamps = {} # user file change time, indexed by canonical path        

        # default path: same folder as printer.cfg
        start_args = self.printer.get_start_args()
        config_file = start_args.get("config_file")
        self.constCONFIG = os.path.dirname(config_file)
        self.constHOME = Path.home()
        self.constTEMP = tempfile.gettempdir()

        self.lastFile = "my_fun.py"
        self.lastPath = self.constCONFIG
        self.lastFun = "my_fun"

        # We use the one-letter "U" macro for concise user code. It's not used in RS‑274 and friends (some CNC machines: secondary X axis)
        self.gcode.register_command(
            'U', self.cmd_U,
            desc="Calls arbitrary user Python code. FUN=(my_fun: fct name) FILE=(my_fun.py: file name) PATH=(location of printer.cfg: file location) CLEAR=(0: resets state)"
        )

    def _initStorage(self):
        self.myFunDict = attrDict() # dict with dot access
        self.myFunDict.printer = self.printer
        self.myFunDict.gcode = self.gcode
        self.myFunDict.hello = self            
        # closure to allow self.log() syntax
        def log(txt):
            self.G("RESPOND TYPE=echo MSG='"+str(txt)+"'")
        def logE(txt):
            self.G("RESPOND TYPE=error MSG='"+str(txt)+"'")
        self.myFunDict.log = log
        self.myFunDict.logE = logE        

    def _U_inner(self, canonicalFilePath, FUN):
        # === change detection ===
        try:
            timestamp = os.path.getmtime(canonicalFilePath)
        except Exception as e:
            self.G("RESPOND TYPE=error MSG='python file "+str(canonicalFilePath)+" not accessible: "+str(e)+"'")
            return 0
            
        if not canonicalFilePath in self.codeTimestamps or not canonicalFilePath in self.codeNamespace or self.codeTimestamps[canonicalFilePath] != timestamp:
            # must (re)compile:
            # - read file
            try:
                source = open(canonicalFilePath).read()
            except Exception as e:
                self.G("RESPOND TYPE=error MSG='reading python file "+str(canonicalFilePath)+" failed:"+str(e)+"'")
                return 0

            # - compile
            try:
                code = compile(source, canonicalFilePath, "exec")
            except Exception as e:
                self.G("RESPOND TYPE=error MSG='compiling python file "+str(canonicalFilePath)+" failed:"+str(e)+"'")
                return 0

            # - run file
            newNs = {}
            try:
                exec(code, newNs)
            except Exception as e:
                self.G("RESPOND TYPE=error MSG='running python file "+str(p)+" failed:"+str(e)+"'")
                return 0
            self.codeNamespace[canonicalFilePath] = newNs

        # === call function ===
        if not FUN in self.codeNamespace[canonicalFilePath]:
            self.G("RESPOND TYPE=error MSG='python file "+str(p)+" does not provide function "+FUN+"'")
            return 0

        try:
            self.codeNamespace[FUN](self.myFunDict, gcmd)
        except Exception as e:
            self.G("RESPOND TYPE=error MSG='fun exec failed:"+str(e)+"'")
            return 0
        return 1 # success
    
    def _subst(self, arg):
        return arg.format(CONFIG=self.constCONFIG, HOME=self.constHOME, TEMP=self.constTEMP)

    def cmd_U(self, gcmd):        
        FILE = gcmd.get("FILE", default=self.lastFile)
        PATH = gcmd.get("PATH", default=None) # deferred: self.lastPath
        FUN = gcmd.get("FUN", default=self.lastFun)
        CLEAR = gcmd.get_bool("CLEAR", default=False)

        FILE = self._subst(FILE)
        # the file argument may bring a path component. 
        # It is handled separately from PATH as it updates self.lastFile, not self.lastPath
        altPath, altFilename = os.path.split(FILE)
        if altPath and altPath.is_absolute():
            if PATH is not None:
                self.G("RESPOND TYPE=error MSG='absolute path in FILE cannot be combined with PATH'")
                return
            canonicalFilePath = Path(os.path.join(PATH, FILE)).resolve()
        else:            
            # deferred default:
            if PATH is None:
                PATH = self.lastPath
            PATH = self._subst(PATH)
            canonicalFilePath = Path(os.path.join(PATH, FILE)).resolve()

        # provide user object (persistent, unless CLEAR is set)
        if CLEAR or self.myFunDict is None:
            self._initStorage()

        if not self._U_inner(self, canonicalFilePath, FUN):
            return # error
        
        # === update defaults on successful fun execution ===
        self.lastPath = PATH
        self.lastFile = FILE
        self.lastFun = FUN          
        
# primary entry point for extension
def load_config(config):
    return klipperHotload(config)