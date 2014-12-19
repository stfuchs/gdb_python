python
import sys
from os.path import expanduser
print ("GDB running Python Version: " + sys.version)
sys.path.append(expanduser('~')+'/git/gdb_python')
#import libstdcxx.v6
from gdbpyext.stl import *
from gdbpyext.eigen import *
from gdbpyext.common import *
end

define ipy_kernel
       python import IPython; IPython.embed_kernel()
end