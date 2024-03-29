#!/usr/bin/env python3

from optparse import OptionParser
import numpy as np

def optP():
    """Parse command line options.
    """

    usage="[python3] %prog -i mol.gro -r POPC -a P"
    description="Membrane leaflet divider"
    version="\n%prog Version 1.0 \n\nRequires Python 3 and Numpy\n" \

    optParser = OptionParser(
                        usage=usage,
                        version=version,
                        description=description
    )

    optParser.set_defaults(molFN=None, resNA=None, atomNA=None)

    optParser.add_option(
                    '-i', type='str',
                     dest='molFN',
                     help="Input 3D structure (gro)"
                     " [default: %default]"
    )

    optParser.add_option(
                    '-r', type='str',
                     dest='resNA',
                     help="Residue membrane component (e.g. POPC)"
                     " [default: %default] "
    )


    optParser.add_option(
                    '-a', type='str',
                     dest='atomNA',
                     help="Atom name for distance calculation (e.g. P)"
                     " [default: %default]"
    )

    options, args = optParser.parse_args()

    if options.molFN == None:
        print("Error: 3D structure (gro) is required.\n")
        sys.exit(1)
    elif options.resNA == None:
        print("Error: Reference residue name is required.\n")
        sys.exit(1)
    elif options.atomNA == None:
        print("Error: Atom name is required.\n")
        sys.exit(1)

    return options, args

def skip_lines(f, i):
    for i in range(i):
        next(f)

def read_gro_line(f_in):
    l = f_in.readline()
    if l == '' or len(l)<45:
        return ''

    # a_number = int(l[15:20])
    # x = float(l[20:28])
    # y = float(l[28:36])

    res_name = l[5:10].strip()
    res_num = int(l[0:5])
    a_name = l[10:15].strip()
    z = float(l[36:44])

    return res_name, res_num, a_name, z

def print_leaflet(fname, res_name, atom_name):
    f = open(fname, 'r')
    skip_lines(f,2)

    upper = np.array([])
    lower = np.array([])
    center = find_center(fname, res_name, atom_name)

    while True:
        try:
            res, res_num, atom, z = read_gro_line(f)
        except ValueError:
            break

        if res == res_name and atom == atom_name:
            if z < center:
                lower = np.append(lower, res_num)
            else:
                upper = np.append(upper, res_num)

    f.close()

    print("\nUpper leaflet (%d residues):\n"%(len(upper)))
    print_consecutive_elems(upper)
    print("\nLower leaflet (%d residues):\n"%(len(lower)))
    print_consecutive_elems(lower)

    print("\nCenter at z = %.3f\n"%(center))

def find_center(fname, res_name, atom_name):
    f = open(fname, 'r')
    skip_lines(f,2)

    z_sum = 0
    z_numb = 0

    while True:
        try:
            res, res_num, atom, z = read_gro_line(f)
        except ValueError:
            break

        if res == res_name and atom == atom_name:
            z_sum += z
            z_numb += 1

    f.close()

    try:
        return z_sum/z_numb
    except ZeroDivisionError:
        print("\nNo matches found. Check res_name and atom_name.\n")
        raise

def print_consecutive_elems(array):
    prev = array[0]
    low = array[0]

    for i in range(1,len(array)):
        if array[i] == prev + 1:
            prev = array[i]
            continue
        else:
            print("%d-%d"%(low, array[i-1]))
            low = array[i]
            prev = array[i]

    print("%d-%d\n"%(low, array[i]))

if __name__ == "__main__":
    options, args = optP()

    print_leaflet(
        options.molFN,
        options.resNA,
        options.atomNA
    )
