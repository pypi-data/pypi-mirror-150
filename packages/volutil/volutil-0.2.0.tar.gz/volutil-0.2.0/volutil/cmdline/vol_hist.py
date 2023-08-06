# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse

import numpy as np
import nibabel as nib

from .. import ihist

description = 'Dump a volume histogram.'

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', help='input volume')

    args = parser.parse_args()

    volume = nib.load(args.input)

    for (value, count) in ihist(volume):
        print(value, count)

    return 0

# eof
