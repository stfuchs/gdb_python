import gdb
import re
import numpy as np

def printEig(mat):
    print(mat['m_storage']['m_data']['array'])

def getType(mat):
    m = re.search("Eigen::Matrix\<(.*)\>",str(mat.type))
    templates = m.group(1).split(",")
    templates = [ t.replace(" ","") for t in templates ]
    return int(templates[1]), int(templates[2])

def eig2numpy(mat):
    # eigen default: column major
    rows,cols = getType(mat)
    a = np.zeros([rows,cols])
    data = mat['m_storage']['m_data']['array']
    for c in range(cols):
        for r in range(rows):
            a[r,c] = float(data[c*rows+r])
    return a

            
