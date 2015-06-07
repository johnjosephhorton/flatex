#!usr/bin/env python
"""
This "flattens" a LaTeX document by replacing all \input{X} lines w/ the
text actually contained in X. See associated README.md for details.
Use as a python module in a python script by saying import flatex then
flatex.main(in file, out file)
"""

import os
import re
import sys


def is_input(line):
    """
    Determines whether or not a read in line contains an uncommented out
    \input{} statement. Allows only spaces between start of line and
    '\input{}'.
    """
    #tex_input_re = r"""^\s*\\input{[^}]*}""" # input only
    tex_input_re = r"""(^[^\%]*\\input{[^}]*})|(^[^\%]*\\include{[^}]*})"""  # input or include
    return re.search(tex_input_re, line)


def get_input(line):
    """
    Gets the file name from a line containing an input statement.
    """
    tex_input_filename_re = r"""{[^}]*"""
    m = re.search(tex_input_filename_re, line)
    return m.group()[1:]


def combine_path(base_path, relative_ref):
    """
    Combines the base path of the tex document being worked on with the the
    relate reference found in that document.
    """
    if (base_path != ""):
        os.chdir(base_path)
    # Handle if .tex is supplied directly with file name or not
    if relative_ref.endswith('.tex'):
        return os.path.join(base_path, relative_ref)
    else:
        return os.path.abspath(relative_ref) + '.tex'


def expand_file(base_file, include_bbl):
    """
    Recursively-defined function that takes as input a file and returns it
    with all the inputs replaced with the contents of the referenced file.
    """
    output_lines = []
    f = open(base_file, "r")
    for line in f:
        if is_input(line):
            new_base_file = combine_path(current_path, get_input(line))
            output_lines += expand_file(new_base_file, include_bbl)
            output_lines.append('\n')  # add a new line after each file input
        else:
            # Optionally replace \bibliography with content of .bbl file
            if include_bbl and line.startswith("\\bibliography"):
                output_lines += bbl_file(base_file)
            else:
                output_lines.append(line)
    f.close()
    return output_lines


def bbl_file(base_file):
    """
    Return content of associated .bbl file
    """
    bbl_path = os.path.abspath(os.path.splitext(base_file)[0]) + '.bbl'
    return open(bbl_path).readlines()


def main(base_file, output_file, include_bbl=False):

    include_bbl = True

    g = open(output_file, "w")
    g.write(''.join(expand_file(base_file, include_bbl)))
    g.close()
    return None


def parse_input(arguments):

    usage = "Usage: python flatex input.tex output.tex [include_bbl]"

    if len(cmd_input) == 2:
        base_file, output_file = arguments
        include_bbl = False
    elif len(cmd_input) == 3:
        base_file, output_file, bib = arguments
        if bib == "include_bbl":
            include_bbl = True
        else:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    return base_file, output_file, include_bbl


if __name__ == '__main__':
    cmd_input = sys.argv[1:]
    base_file, output_file, include_bbl = parse_input(cmd_input)
    current_path = os.path.split(base_file)[0]
    main(base_file, output_file, include_bbl)
