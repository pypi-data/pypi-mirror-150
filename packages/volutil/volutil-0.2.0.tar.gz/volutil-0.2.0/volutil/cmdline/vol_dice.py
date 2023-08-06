# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse
import csv

import numpy as np
import nibabel as nib

from .. import load_lut, ihist

description = 'Calculate Dice coefficients for ROI overlaps.'

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--lut', '-l', help='LUT')
    parser.add_argument('--force-overwrite', '-f')
    parser.add_argument('input_1', help='input volume 1')
    parser.add_argument('input_2', help='input volume 2')
    parser.add_argument('output', help='output CSV', nargs='?')

    args = parser.parse_args()

    if args.force_overwrite and args.ouptput and os.path.exists(args.output):
        print(f'{progname}: {args.output} exists', file=sys.stderr)
        return 1

    print(f'reading {args.input_1}...')
    vol_1 = nib.load(args.input_1)

    print(f'reading {args.input_2}...')
    vol_2 = nib.load(args.input_2)

    if vol_1.shape != vol_2.shape:
        print(
            f'{progname}: volumes do not have the same shape', 
            file=sys.stderr
        )
        sys.exit(1)

    if args.lut:
        lut = load_lut(args.lut)

    data_1 = np.array(np.rint(vol_1.get_fdata()), dtype='int')
    data_2 = np.array(np.rint(vol_2.get_fdata()), dtype='int')

    values = range(
        min(data_1.min(), data_2.min()), 
        max(data_1.max(), data_2.max()) + 1
    )

    if args.output:
        f = open(args.output, 'w')
    else:
        f = sys.stdout
    try:
        writer = csv.writer(f)
        if args.lut:
            headers = ['Index', 'Structure', 'Dice coefficient']
        else:
            headers = ['Index', 'Dice coefficient']
        writer.writerow(headers)
        for value in values:
            a = (data_1==value).sum()
            b = (data_2==value).sum()
            if a == 0 and b == 0:
                continue
            ab = ((data_1==value)&(data_2==value)).sum()
            coef = 2*ab/(a+b)
            if args.lut:
                row = [value, lut.get(value, [''])[0], coef]
            else:
                row = [value, coef]
            writer.writerow(row)
    finally:
        f.close()

    return 0

# eof
