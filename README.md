flatex.py 
---------

This "flattens" a LaTeX document by replacing all `\input{X}` lines with the text actually contained in X. It uses the `click` module to create a command line interface. 

Two new options are available:
- Specify a .tex subfolder for input files similarly to what the `input@path` command does in the main file
- Launch an interactive session to allow the user to select only specific sections to import

It was inspired by [this discussion on Stack Overflow](http://tex.stackexchange.com/questions/21838/replace-inputfilex-by-the-content-of-filex-automatically/21840#21840). There are C and perl versions of this, but I wanted a pure python version to fit in with my existing paper-creating toolchain.  

To install
----------
    git clone https://github.com/giovannibonaccorsi/flatex.git
    cd flatex
    pip install --editable . 

Usage
-----------------------------
As a stand-alone script:

    flatex inputfile.tex outputfile.tex

If you want to include the bbl file as well:

    flatex --include_bbl inputfile.tex outputfile.tex

If you want to specify a .tex subfolder: 

    flatex inputfile.tex outputfile.tex --tex_folder folder_name

If you want to select only specific input files to expand:

    flatex inputfile.tex outputfile.tex --interactive



Limitations: 
------------

1. It does also recognize `\includes` commands, but this has not been tested. 
1. Tested for nested inputs, although not extensively (only two levels deep). 
1. Tested for file living in subdirectories, only one level deep. 
1. The test case writes to the /tmp folder - so the test probably
   wouldn't work on Windows(?). 
   

Copyright, 2015, John J. Horton (john.joseph.horton@gmail.com)
Distributed under the terms of the GNU General Public License
See http://www.gnu.org/licenses/gpl.txt for details. 
