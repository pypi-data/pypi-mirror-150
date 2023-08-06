# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse

import nibabel as nib

description = 'Show basic statistics of a volume.'

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', help='input volume')

    args = parser.parse_args()

    volume = nib.load(args.input)

    data = volume.get_fdata()

    print('min:', data.min())
    print('max:', data.max())
    print('mean:', data.mean())
    print('std:', data.std())

    return 0

# eof
