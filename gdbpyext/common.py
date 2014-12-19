import gdb
import re
from gdbpyext.consolecolors import cc as colorize

class Variable(gdb.Value):
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        stype = highlight_type(self.type.strip_typedefs().__str__())
        return "%s (%s)"%(gdb.Value.__str__(self), stype)

    def __getitem__(self,key):
        return Variable(gdb.Value.__getitem__(self,key))

    def cast(self,type):
        return Variable(gdb.Value.cast(self,type))

def print_variable(v, intend="",prefix="",is_base=False):
    v = Variable(v)
    vtype = v.type.strip_typedefs()

    if vtype.code == gdb.TYPE_CODE_STRUCT:
        cvtype = highlight_type(str(vtype))
        if not is_base: print("%s%s (%s):" % (intend, prefix, cvtype))
        for key in vtype:
            #print gdb.lookup_symbol(key), key
            #if gdb.lookup_symbol(key)[0] == None: continue
            try:
                basetype = gdb.lookup_type(key).strip_typedefs()
                print_variable(v.cast(basetype), intend, prefix, True)
            except gdb.error as err:
                try:
                    vkey = v[key]
                except gdb.error as err:
                    continue
                ckey = colorize.w(key,color=colorize.c.red)
                print_variable(vkey, intend+"  ", ckey)
    else:
        print("%s%s = %s" % (intend, prefix, v) )

def print_type_hierarchy(t, intend=""):
    tt = t.strip_typedefs()
    if tt.code == gdb.TYPE_CODE_STRUCT:
        ctt = highlight_type(str(tt))
        print("%s<%s>" % (intend, ctt))
        for key in tt:
            try:
                basetype = gdb.lookup_type(key).strip_typedefs()
                print_type_hierarchy(basetype, intend+"  ")
            except gdb.error:
                continue

def highlight_type(stype):
    split1 = stype.split("<",1)
    if len(split1) > 1:
        split2 = split1[1].rsplit("::",1)
        if len(split2) > 1 and split2[1][-1]!=">":
            split1[1] = split2[0] + "::" + colorize.w(split2[1],color=colorize.c.blue)
        split1[0] = colorize.w(split1[0],color=colorize.c.green) + "<" + split1[1]
    else:
        split1[0] = colorize.w(split1[0],color=colorize.c.green)
    return split1[0]

def py(symbol):
    "converts gdb symbol to python object gdb.Value"
    return Variable(gdb.parse_and_eval(symbol))

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

def cb(filename=""):
    if filename != "":
        print(gdb.execute("break "+filename, to_string=True))
    else:
        for r in c("info break").split("\n")[1:]:
            colorizeFrame(r,False)

def cq():
    gdb.execute("quit")

