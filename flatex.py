#!/usr/bin/env python

# flatex.py 

#  This "flattens" a LaTeX document by replacing all 
#  \input{X} lines w/ the text actually contained in X. 

# Inspired by: 
# http://tex.stackexchange.com/questions/21838/replace-inputfilex-by-the-content-of-filex-automatically/21840#21840
# (there are C and per versions of this, but I wanted a pure python 
# version to fit in w/ my existing paper-creating toolchain) 

# To use as a stand-alone script, call: 
# >>> python flatten.py inputfile.tex outputfile.tex 

# Copyright, 2012, John J. Horton (john.joseph.horton@gmail.com)
# Distributed under the terms of the GNU General Public License
# See http://www.gnu.org/licenses/gpl.txt for details. 

# Limitations: 

# It doesn't do \includes - just inputs. 

# I haven't tested it for nested inputs (thought it's designed
# to work on files like). 

# I haven't tested it for  more complicated file arrangements 
# e.g., realtive reference inputs that are more complex that just 
# a file living in the same directory. 

# I haven't tested it on anything other than Ubunut Linux 10

# The test case writes to the /tmp folder - so the test probably
# wouldn't work on Windows(?). 

import os 
import re 
import sys

def is_input(line):
    """
    Determines whether or not a read in line contains an 
uncommented out \input{} statement. Allows only spaces between 
start of line and '\input{}'. 
    """
    tex_input_re = r"""^\s*\\input{[^}]*}"""
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
    Combines the base path of the tex document being worked on 
with the the relate reference found in that document.  
    """
    return os.path.join(base_path, relative_ref)

def expand_file(base_file):
    """
    Recursively-defined function that takes as input a file and 
returns it with all the inputs replaced with the contents of the 
referenced file.  
    """
    output_lines = [] 
    f = open(base_file, "r")
    for line in f:
        if is_input(line):
            current_path = os.path.split(base_file)[0] 
            new_base_file = combine_path(current_path, get_input(line))
            output_lines += expand_file(new_base_file)
        else:
            output_lines.append(line)
    f.close() 
    return output_lines 

def main(base_file, output_file): 
    g = open(output_file, "w")
    g.write(''.join(expand_file(base_file)))
    g.close() 
    return None 

if __name__ == '__main__': 
    base_file, output_file = sys.argv[1:]
    main(base_file, output_file)
