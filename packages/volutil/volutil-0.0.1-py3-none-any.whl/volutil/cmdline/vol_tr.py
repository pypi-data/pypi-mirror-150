# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse

import numpy as np
import nibabel as nib

description = 'Change volume values.'
epilog = """
Values are translated according to the mapping given in the map
file and/or value mappings given at the command line.  Map files
should contain space-separated pairs of integers.  Arguments to
"--tr" should be two comma-separated integers.  If both --map and
--tr are given, command-line mappings (--tr) take precedence.
"""

def arg_mapping(s):
    try:
        (v0, v1) = [ int(v) for v in s.split(',') ]
    except ValueError:
        raise argparse.ArgumentTypeError(f'bad value mapping "{s}"')
    return (v0, v1)

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--map', '-m', help='map file')
    parser.add_argument('--tr', '-t', 
                        default=[], 
                        action='append', 
                        type=arg_mapping, 
                        help='map value')
    parser.add_argument('--force-write', '-f', 
                        action='store_true', 
                        help='force overwrite of output if it exists')
    parser.add_argument('input', help='input volume')
    parser.add_argument('output', help='output volume')

    args = parser.parse_args()

    if os.path.exists(args.output) and not args.force_write:
        print(f'{progname}: {args.output} exists', file=sys.stderr)
        sys.exit(1)

    if not args.map and not args.tr:
        print(f'{progname}: warning: no mappings defined', file=sys.stderr)

    map = {}
    if args.map:
        print(f'reading {args.map}...')
        with open(args.map) as f:
            for (line_no, line) in enumerate(f, 1):
                if '#' in line:
                    line = line[:line.index('#')]
                line = line.strip()
                if not line:
                    continue
                line = line.replace(',', ' ')
                try:
                    (v0, v1) = [ int(v) for v in line.split() ]
                except ValueError:
                    msg = f'{progname}: bad mapping on line {line_no} of {args.map}'
                    print(msg, file=sys.stderr)
                    sys.exit(1)
                map[v0] = v1

    map.update(dict(args.tr))

    print(f'reading {args.input}...')
    vol = nib.load(args.input)

    orig_data = vol.get_fdata()
    data = np.zeros(orig_data.shape, dtype=orig_data.dtype)
    vals_set = np.zeros(orig_data.shape, dtype=bool)
    for v0 in sorted(map):
        v1 = map[v0]
        ind = orig_data == v0
        data[ind] = v1
        vals_set |= ind
        if args.verbose:
            n = ind.sum()
            print(f'{v0} -> {v1}: {n}')
    not_set = np.logical_not(vals_set)
    n = not_set.sum()
    if args.verbose:
        print(f'unchanged: {n}')
    data[not_set] = orig_data[not_set]

    vol2 = vol.__class__(data, vol.affine, vol.header)
    print(f'writing {args.output}...')
    nib.loadsave.save(vol2, args.output)

    return 0

# eof
