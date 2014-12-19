import gdb
import gdbpyext.common as gc

def xVecElement(vec, i):
    "return the i'th element of vec"
    return gc.Variable( ((vec['_M_impl']['_M_start']) + i).dereference() )

def xVec(vec):
    "extracts gdb.Value objects from stl vector to python array"
    n =  int(vec['_M_impl']['_M_finish'] - vec['_M_impl']['_M_start'])
    return [ xVecElement(vec, i) for i in range(n) ]
