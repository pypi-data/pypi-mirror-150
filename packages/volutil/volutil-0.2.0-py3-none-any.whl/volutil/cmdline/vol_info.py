# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse

import nibabel as nib

description = 'Print information about a volume.'

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', help='input volume')

    args = parser.parse_args()

    volume = nib.load(args.input)

    print(volume.ndim)
    print(volume.shape)
    print(volume.affine)
    print(volume.get_data_dtype())
    print(volume.header)

    return 0

# eof
