import gdb

def py(symbol):
    "converts gdb symbol to python object gdb.Value"
    return gdb.parse_and_eval(symbol)
