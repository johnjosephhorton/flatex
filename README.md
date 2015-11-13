flatex.py 
---------

This "flattens" a LaTeX document by replacing all \input{X} lines w/ the text actually contained in X. 
I recently re-factored it to use the `click` module to create a command line interface. 

Copyright, 2015, John J. Horton (john.joseph.horton@gmail.com)
Distributed under the terms of the GNU General Public License
See http://www.gnu.org/licenses/gpl.txt for details. 

It was inspired by: 
http://tex.stackexchange.com/questions/21838/replace-inputfilex-by-the-content-of-filex-automatically/21840#21840

There are C and perl versions of this, but I wanted a pure python version to fit in w/ my existing paper-creating toolchain.  

To install
----------
    git clone git@github.com:johnjosephhorton/flatex.git
    cd flatex
    pip install --editable . 

To use as a stand-alone script
-----------------------------
    flatex inputfile.tex outputfile.tex

If you want to include the bbl file as well
--------------------------------------------

    flatex --include_bbl inputfile.tex outputfile.tex


Limitations: 
------------

1) It doesn't do \includes - just inputs. 

2) I haven't tested it for nested inputs (thought it's designed
to work on files like). 

3) I haven't tested it for  more complicated file arrangements 
  e.g., realtive reference inputs that are more complex that just 
  a file living in the same directory. 

4) The test case writes to the /tmp folder - so the test probably
   wouldn't work on Windows(?). 
   
