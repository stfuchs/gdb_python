python
import sys
from os.path import expanduser
sys.path.insert(0, expanduser('~')+'/git/gdb_python')
from libstdcxx.v6.printers import register_libstdcxx_printers
#register_libstdcxx_printers (None)
from gdb_helpers.stl import *
from gdb_helpers.eigen import *
from gdb_helpers.common import *
end