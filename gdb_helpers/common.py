import gdb
import re
from gdb_helpers.ConsoleColors import cc as colorize

class Value(gdb.Value):
    def __repr__(self):
        return "%s %s" % (self.type.__str__(), self.__str__())


def print_class(s, child=""):
    if child == "": child = str(s.type)
    for key in s.type:
        #print("%s.%s" % (s.type,key))
        try:
            t = gdb.lookup_type(key)
            print_class(s.cast(t),child+"::"+key)
        except:
            print("%s::%s = %s" % (child, key, Value(s[key]) ))


def py(symbol):
    "converts gdb symbol to python object gdb.Value"
    return Value(gdb.parse_and_eval(symbol))

def getSymbols(location):
    res = gdb.execute("info scope "+location, to_string=True)
    return [ s.split(" ", 1)[0] for s in res.split("Symbol ")[1:] ]

def colorizeFrame(frame, validate=True):
    code = "\n"
    try: 
        number = re.search("^(#\d+)\s",frame).group(1)
        frame = frame.replace(number, colorize.w(number, color=colorize.c.red))
    except: 
        if validate: return
    try:
        function = re.search("\sin\s(.+)\s\(",frame).group(1)
        frame = frame.replace(function, colorize.w(function, color=colorize.c.green))
    except: None
    try:
        matches = re.search("\/(\w+\.(c|cpp|hpp|h|hh)\:(\d+))",frame)
        filename = matches.group(1)
        line = matches.group(3)
        frame = frame.replace(filename, colorize.w(filename, color=colorize.c.blue))
        code = "\n"+gdb.execute("list "+filename, to_string=True)
        codeline = re.search(line+".+\n",code).group(0)
        code = code.replace(codeline,colorize.w(codeline, color=colorize.c.cyan))
    except: None
    print(frame+code)

def c(command):
    return gdb.execute(command, to_string=True)

def cfile(filename):
    "executes file command to load binary file in gdb"
    print(gdb.execute("file "+filename,to_string=True))

def cbt():
    print(gdb.execute("bt", to_string=True))

def cbth():
    trace = gdb.execute("bt", to_string=True)
    trace = trace.split("\n")
    for f in trace:
        colorizeFrame(f)

def cframe(idx=""):
    frame = gdb.execute("frame "+str(idx), to_string=True)
    colorizeFrame(frame)

def cr():
    frame = gdb.execute("run", to_string=True)
    colorizeFrame(frame, False)

def cn(n=1):
    print([ gdb.execute("next", to_string=True) for i in range(n) ])

def cs(n=1):
    print([ gdb.execute("step", to_string=True) for i in range(n) ])

def cc():
    print(gdb.execute("continue", to_string=True))

def cb(filename):
    print(gdb.execute("break "+filename, to_string=True))

def cq():
    gdb.execute("quit")

