import gdb

def py(symbol):
    "converts gdb symbol to python object gdb.Value"
    return gdb.parse_and_eval(symbol)

def listSymbols(location):
    res = gdb.execute("info scope "+location, to_string=True)
    res = res.rsplit("Symbol ")[1:]
    return [ s.split(maxsplit=1)[0] for s in res ]

def cFile(filename):
    "executes file command to load binary file in gdb"
    print(gdb.execute("file "+filename,to_string=True))

def cBt():
    print(gdb.execute("bt", to_string=True))

def cN(n=1):
    print([ gdb.execute("next", to_string=True) for i in range(n) ])

def cS(n=1):
    print([ gdb.execute("step", to_string=True) for i in range(n) ])

def cC():
    print(gdb.execute("continue", to_string=True))

def cB(filename):
    print(gdb.execute("break "+filename, to_string=True))

def cQuit():
    gdb.execute("quit")

