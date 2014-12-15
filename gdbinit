python
import sys
from os.path import expanduser
print ("GDB running Python Version: " + sys.version)
sys.path.append(expanduser('~')+'/git/gdb_python')
#sys.path.append("/usr/local/lib/python2.7/dist-packages")
import libstdcxx.v6
from gdb_helpers.stl import *
from gdb_helpers.eigen import *
from gdb_helpers.common import *
end

define ipy_kernel
       python import IPython; IPython.embed_kernel()
end