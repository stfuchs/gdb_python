import gdb

def vec_element(vec, i):
    "return the i'th element of vec"
    return ((vec['_M_impl']['_M_start']) + i).dereference()

def vec_to_py(vec):
    "converts stl vector to python array"
    n =  vec['_M_impl']['_M_finish'] - vec['_M_impl']['_M_start']
    return [ vec_element(vec, i) for i in range(n) ]
