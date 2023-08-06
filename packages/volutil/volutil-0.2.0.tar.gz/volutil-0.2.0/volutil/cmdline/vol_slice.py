# See file COPYING distributed with volutil for copyright and license.

import sys
import os
import argparse
import collections

import numpy as np
import nibabel as nib
from nibabel import processing
import PIL.ImageDraw

from .. import load_lut

def arg_volume(fname):
    try:
        vol = nib.load(fname)
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f'{fname}: file not found')
    except nib.filebasedimages.ImageFileError:
        raise argparse.ArgumentTypeError(f'{fname}: unknown volume format')
    if len(vol.shape) != 3:
        msg = 'volume must have exactly three dimensions'
        raise argparse.ArgumentTypeError(msg)
    return vol

def arg_direction_string(arg):
    d = arg.lower()
    if not all(c in 'sca' for c in d):
        raise argparse.ArgumentTypeError(f'bad direction string "{arg}"')
    return d

def get_fov(vol):
    """Get the field of view of a volume.

    We define the field of view as the greatest range along a storage axis, 
    which is the greatest magnitude of:

        d_i = M [ n_i  0   0  ] - M [ 0 0 0 ]

        d_j = M [  0  n_j  0  ] - M [ 0 0 0 ]

        d_k = M [  0   0  n_k ] - M [ 0 0 0 ]

    This reduces to:

              [ n_i  0   0  ]
        D = M [  0  n_j  0  ]
              [  0   0  n_k ]

    We then take the maximum magnitude of the columns of D.
    """
    M = vol.affine[:3,:3]
    D = np.matmul(M, np.eye(3) * vol.shape)
    return max(np.linalg.norm(D, axis=0))

def create_image(vol, tl, tr, bl, size, lut=None):
    """Resample a volume to a 2D image.

    Arguments are the volume, three 3-element sequences giving the
    RAS coordinates of the top left (tl), top right (tr), and bottom
    left (br) pixels, and an image size (a single integer).

    There is also an optional LUT (colormap) argument.

    Our approach is to use nibabel.processing.resample_from_to()
    to sample the volume to a size x size x 1 volume.  For the
    output transformation M, tl (where (i, j, k) = (0, 0, 0)) give
    us the translation parameters, and the first and second column,
    which map i and j, respectively, are simply (tr-tl)/(size-1)
    and (br-tl)/(size-1).

    We're free to choose the mapping of k since we're not going to
    sample off the k=0 plane.  To keep things well-behaved, we
    choose the direction as the cross product of the i and j mapping
    vectors and the magnitude to be the geometric mean of the
    magnitude of these vectors.

    So:

            [  |   |   |   |  ]
        M = [ M_i M_j M_k M_t ]
            [  |   |   |   |  ]
            [  0   0   0   1  ]

    where:

        M_i = (tr-tl)/(size-1)

        M_j = (bl-tl)/(size-1)

        M_k = M_i x M_j / sqrt(|M_i| * |M_j|)

        M_t = tl

    The mode of the output image is L, or RGBA if lut is given.
    """
    tl = np.array(tl)
    tr = np.array(tr)
    bl = np.array(bl)
    m_i = (tr-tl)/(size-1)
    m_j = (bl-tl)/(size-1)
    m_k = np.cross(m_i, m_j)/np.sqrt(np.linalg.norm(m_i)*np.linalg.norm(m_j))
    M = np.vstack((m_i, m_j, m_k, tl))
    M = np.transpose(M)
    M = np.vstack((M, [0, 0, 0, 1]))
    to_vox_map = ((size, size, 1), M)
    # nearest neighbor resampling if we have LUT; otherwise trilinear 
    # interpolation
    order = 0 if lut else 1
    im = nib.processing.resample_from_to(vol, to_vox_map, order=order)
    # preserve the integer type if we're going to apply a colormap
    data = np.asanyarray(im.dataobj) if lut else im.get_fdata()
    data.shape = (size, size)
    data = data.transpose()
    if lut:
        im = PIL.Image.fromarray(np.array(data, dtype='uint8'))
        palette = [0, 0, 0, 0]
        for index in range(1, 256):
            if index in lut:
                palette.extend(list(lut[index][1:]) + [255])
            else:
                palette.extend([0, 0, 0, 0])
        im.putpalette(palette, rawmode='RGBA')
        im = im.convert('RGBA')
    else:
        data = np.array(data, dtype=float)
        data = data - data.min()
        data = data / (data.max()-data.min()) * 255
        data = np.array(data, dtype='uint8')
        im = PIL.Image.fromarray(data)
    return im

description = 'Slice volumes to 2D images.'

epilog = """
A LUT must take the form of a FreeSurfer color file, with columns
index, label, R, G, B, and alpha (alpha is ignored).  Only eight
bits of overlay are supported.  The direction string indicates which
slice planes to generate (sagittal, coronal, axial) and defaults
to SCA.
"""

def main():

    progname = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('base_volume', 
                        type=arg_volume, 
                        metavar='input', 
                        help='base volume')
    parser.add_argument('--base-lut', '-l', 
                        help='base volume LUT file')
    parser.add_argument('--overlay', '-O', 
                        type=arg_volume, 
                        help='overlay volume')
    parser.add_argument('--overlay-lut', '-L', 
                        help='overlay volume LUT file')
    parser.add_argument('--size', '-s', type=int, help='image size')
    parser.add_argument('--directions', '-d', 
                        type=arg_direction_string, 
                        default='sca', 
                        help='slice direction(s)')
    parser.add_argument('--suppress-labels', '-S', 
                        dest='labels', 
                        default=True, 
                        action='store_false', 
                        help='suppress orientation labels')
    parser.add_argument('--force-overwrite', '-f', 
                        action='store_true', 
                        help='force overwrite of output file')
    parser.add_argument('output', help='output image')

    args = parser.parse_args()

    if args.base_lut:
        base_lut = load_lut(args.base_lut)
    else:
        base_lut = None

    overlay_lut = None
    if args.overlay and args.overlay_lut:
        overlay_lut = load_lut(args.overlay_lut)

    if os.path.exists(args.output) and not args.force_overwrite:
        print(f'{progname}: {args.output} exists', file=sys.stderr)
        sys.exit(1)

    fov = get_fov(args.base_volume)

    if args.size:
        size = args.size
    else:
        size = max(args.base_volume.shape)

    # calculate the low/mid/high coordinates
    mid_ijk = np.append(np.array(args.base_volume.shape) / 2, 1)
    mid_ras = np.matmul(args.base_volume.affine, mid_ijk)

    Range = collections.namedtuple('Range', ['low', 'mid', 'high'])
    r = Range(mid_ras[0]-fov/2, mid_ras[0], mid_ras[0]+fov/2)
    a = Range(mid_ras[1]-fov/2, mid_ras[1], mid_ras[1]+fov/2)
    s = Range(mid_ras[2]-fov/2, mid_ras[2], mid_ras[2]+fov/2)

    images = []
    for direction in args.directions:
        if direction == 's':
            tl = [r.mid, a.low, s.high]
            tr = [r.mid, a.high, s.high]
            bl = [r.mid, a.low, s.low]
            labels = ['S', 'A', 'I', 'P']
        if direction == 'c':
            tl = [r.high, a.mid, s.high]
            tr = [r.low, a.mid, s.high]
            bl = [r.high, a.mid, s.low]
            labels = ['S', 'L', 'I', 'R']
        if direction == 'a':
            tl = [r.high, a.high, s.mid]
            tr = [r.low, a.high, s.mid]
            bl = [r.high, a.low, s.mid]
            labels = ['A', 'L', 'P', 'R']
        base_image = create_image(args.base_volume, tl, tr, bl, size, base_lut)
        # create_image() will give us an image with transparency if we give a 
        # colormap; we remove the transparency on the base image
        if base_image.mode == 'RGBA':
            base_image = base_image.convert('RGB')
        if args.overlay:
            overlay_image = create_image(
                args.overlay, 
                tl, 
                tr, 
                bl, 
                size, 
                overlay_lut
            )
            image = PIL.Image.composite(
                overlay_image, 
                base_image.convert('RGBA'), 
                overlay_image
            )
        else:
            image = base_image
        if args.labels:
            fill = (255, 255, 255) if image.mode in ('RGB', 'RGBA') else 255
            draw = PIL.ImageDraw.Draw(image)
            draw.text((size/2, 10), labels[0], fill=fill, anchor='mm')
            draw.text((size-10, size/2), labels[1], fill=fill, anchor='mm')
            draw.text((size/2, size-10), labels[2], fill=fill, anchor='mm')
            draw.text((10, size/2), labels[3], fill=fill, anchor='mm')
        images.append(image)

    composite = PIL.Image.new(images[0].mode, (size*len(images), size))

    for (i, image) in enumerate(images):
        box = (i*size, 0, (i+1)*size, size)
        composite.paste(image, box)

    composite.save(args.output)

    return 0

# eof
