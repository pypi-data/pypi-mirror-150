# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse
import functools
import operator

import numpy as np
import nibabel as nib

description = 'Dump voxel values in volumes.'

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--suppress-indices', '-s', action='store_true')
    parser.add_argument('inputs', help='input volume(s)', nargs='+')

    args = parser.parse_args()

    data = []
    for fname in args.inputs:
        print(f'loading {fname}...', file=sys.stdout)
        vol = nib.load(fname)
        if len(data) > 1 and data.shape != data[0].shape:
            print(f'{progname}: volume shape mismatch', file=sys.stderr)
            sys.exit(1)
        d = vol.get_fdata()
        d = np.moveaxis(d, range(d.ndim), reversed(range(d.ndim)))
        data.append(d)

    n_vals = functools.reduce(operator.mul, data[0].shape)

    for inds in zip(*np.unravel_index(range(n_vals), data[0].shape)):
        vals = [ d[inds] for d in data ]
        if args.suppress_indices:
            print(*vals)
        else:
            print(*reversed(inds), *vals)

    return 0

# eof
