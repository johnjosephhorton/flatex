import click
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
    Combines the base path of the tex document being worked on with the
    relate reference found in that document.
    """
    if (base_path != ""):
        os.chdir(base_path)
    # Handle if .tex is supplied directly with file name or not
    if relative_ref.endswith('.tex'):
        return os.path.join(base_path, relative_ref)
    else:
        return os.path.abspath(relative_ref) + '.tex'



def expand_file(start_base_file, base_file, current_path, include_bbl, noline, nocomment,no_image_path):
    """
    Recursively-defined function that takes as input a file and returns it
    with all the inputs replaced with the contents of the referenced file.
    """
    output_lines = []
    f = open(base_file, "r",encoding='utf-8')
    for line in f:
        if is_input(line):
            new_base_file = combine_path(current_path, get_input(line))
            output_lines += expand_file(start_base_file, new_base_file, current_path, include_bbl, noline, nocomment,no_image_path)
            if noline:
                pass
            else:
                output_lines.append('\n')  # add a new line after each file input
        elif include_bbl and line.startswith("\\bibliography") and (not line.startswith("\\bibliographystyle")):
            output_lines += bbl_file(start_base_file)
        elif nocomment and len(line.lstrip()) > 0 and line.lstrip()[0] == "%":
            pass
        elif no_image_path and "includegraphics" in line:
            new_line = remove_image_path(line)
            output_lines.append(new_line)
        else:
            output_lines.append(line)
    f.close()
    return output_lines

def remove_image_path(line):
    pattern = r"{.*/([a-zA-Z].*)}"  # Capture filename between last / and }
    new_line = re.sub(pattern, r"{\1}", line)
    return new_line


def bbl_file(start_base_file):
    """
    Return content of associated .bbl file
    """
    bbl_path = os.path.abspath(os.path.splitext(start_base_file)[0]) + '.bbl'
    return open(bbl_path).readlines()


@click.command()
@click.argument('base_file', type = click.Path())
@click.argument('output_file', type = click.Path())
@click.option('--include_bbl/--no_bbl', default=False)
@click.option("--noline", is_flag = True)
@click.option("--nocomment", is_flag = True
              , help="""remove any line that is a comment 
                    (this will preserve comments"
                        "at the same line as the text)""")
@click.option("--no_image_path", is_flag = True)
def main(base_file, output_file, include_bbl=False, noline=False, nocomment=False, no_image_path=False):
    
    """
    This "flattens" a LaTeX document by replacing all \input{X} lines w/ the
    text actually contained in X. See associated README.md for details.
    """
    current_path = os.path.split(base_file)[0]
    g = open(output_file, "w", encoding='utf-8')
    lines = expand_file(base_file, base_file, current_path, include_bbl,
                        noline, nocomment,no_image_path)
    content = ''.join(lines)
    g.write(content)
    g.close()
    return None



