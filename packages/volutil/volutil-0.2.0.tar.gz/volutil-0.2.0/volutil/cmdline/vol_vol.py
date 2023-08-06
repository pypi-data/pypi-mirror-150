# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse
import csv

import numpy as np
import nibabel as nib

from .. import load_lut, ihist

description = 'Calculate volumes of ROIs.'

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--lut', '-l', help='LUT')
    parser.add_argument('--force-overwrite', '-f')
    parser.add_argument('input', help='input volume')
    parser.add_argument('output', help='output CSV', nargs='?')

    args = parser.parse_args()

    if args.force_overwrite and args.ouptput and os.path.exists(args.output):
        print(f'{progname}: {args.output} exists', file=sys.stderr)
        return 1

    print(f'reading {args.input}...')
    vol = nib.load(args.input)

    if args.lut:
        lut = load_lut(args.lut)

    if args.output:
        f = open(args.output, 'w')
    else:
        f = sys.stdout
    try:
        writer = csv.writer(f)
        if args.lut:
            headers = ['Index', 'Structure', 'Voxels', 'Volume']
        else:
            headers = ['Index', 'Voxels', 'Volume']
        writer.writerow(headers)
        det = abs(np.linalg.det(vol.affine))
        for (value, count) in ihist(vol):
            if args.lut:
                row = [value, lut.get(value, [''])[0], count, det*count]
            else:
                row = [value, count, det*count]
            writer.writerow(row)
    finally:
        f.close()

    return 0

# eof
