# See file COPYING distributed with volutil for copyright and license.

import numpy as np

__version__ = '0.2.0'

def load_lut(fname):
    """Load and validate a FreeSurfer look up table, reporting errors."""
    lut = {}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            (index, label, r, g, b, _) = line.split()
            (index, r, g, b) = map(int, (index, r, g, b))
            lut[index] = (label, r, g, b)
    return lut

def ihist(vol):
    """Create a histogram with integer bins."""
    data = np.array(np.rint(vol.get_fdata()), dtype='int')
    edges = np.arange(data.min() - 0.5, data.max() + 0.5 + 1)
    (counts, _) = np.histogram(data, edges)
    return list(zip((int(e+0.5) for e in edges[:-1]), counts))

# eof
