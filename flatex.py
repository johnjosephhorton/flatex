import os
import re
import click

def is_input(line, include_too=True):
    """
    Determines via regex whether or not a line from file contains an
    uncommented \\input{} statement. Allows only spaces between start
    of line and '\\input{}'.
    """
    if include_too:
        # input or include (not tested)
        tex_input_re = r"""(^[^\%]*\\input{[^}]*})|(^[^\%]*\\include{[^}]*})"""
    else:
        # input only
        tex_input_re = r"""^\s*\\input{[^}]*}"""
    return re.search(tex_input_re, line)


def get_input(line):
    """
    Gets the file name from a line containing an input statement.
    """
    tex_input_filename_re = r"""{[^}]*"""
    matched_text = re.search(tex_input_filename_re, line)
    return matched_text.group()[1:]


def combine_path(base_path, relative_ref, tex_folder):
    """
    Combines the base path of the tex document being worked on with the
    relate reference found in that document.

    Use specific .tex folder if provided by the user.
    """
    if base_path:
        os.chdir(base_path)
    # avoid duplicating tex_folder
    if tex_folder and tex_folder in relative_ref:
        tex_folder = ''
    # Handle if .tex is supplied directly with file name or not
    if relative_ref.endswith('.tex'):
        return os.path.join(base_path, tex_folder, relative_ref)
    else:
        return os.path.abspath(os.path.join(tex_folder, relative_ref))+'.tex'


def expand_file(base_file, current_path, include_bbl, noline, tex_folder, interactive):
    """
    Recursively-defined function that:
    - takes as input a file and opens it
    - looks for 'input' or 'include' commands and get their file references
    - analyze the references for further commands (recursively)
    - then expands their content inside the main tex, appending it
    - and return the complete file

    With the interactive option the user is allowed to chose which file to
    expand (if maybe some section are still worked on, or don't need to be added.)
    """
    output_lines = []
    with open(base_file, "r") as file_to_read:
        for line in file_to_read:
            bbl_flag = (
                line.startswith("\\bibliography")
                and (not line.startswith("\\bibliographystyle")))
            if is_input(line):
                input_str = get_input(line)
                if interactive:
                    prompt_q = "Expand this section (Y or yes to proceed)?\n {}\n".format(input_str)
                    user_input = raw_input(prompt_q) # Python 3 incompatibility
                    user_input = user_input.lower()
                    proceed = True if (
                        user_input == 'y' or user_input == 'yes') else False
                else:
                    proceed = True
                if proceed:
                    new_base_file = combine_path(current_path, input_str, tex_folder)
                    output_lines += expand_file(
                        new_base_file, current_path, include_bbl,
                        noline, tex_folder, interactive)
                    # add a new line after each file input
                    if noline:
                        pass
                    else:
                        output_lines.append('\n')
                else:
                    output_lines.append(line)
            elif include_bbl and bbl_flag:
                output_lines += bbl_file(base_file)
            else:
                output_lines.append(line)
    return output_lines


def bbl_file(base_file):
    """
    Return content of associated .bbl file
    """
    bbl_path = os.path.abspath(os.path.splitext(base_file)[0]) + '.bbl'
    return open(bbl_path).readlines()


@click.command()
@click.argument('base_file', type=click.Path())
@click.argument('output_file', type=click.Path())
@click.option('--include_bbl/--no_bbl', default=False)
@click.option('--noline', is_flag=True)
@click.option('--tex_folder', default='')
@click.option('--interactive', is_flag=True, default=False)
def main(
    base_file, output_file, include_bbl=False,
    noline=False, tex_folder='', interactive=False):
    """
    This "flattens" a LaTeX document by replacing all \\input{X} lines w/ the
    text actually contained in X. See associated README.md for details.

    If .tex files are placed in a specific folder via input@path command in
    the preamble of the latex file the tex_folder option must be specified.

    Input:
    base_file:      (str)   main .tex file to explore
    output_file:    (str)   .tex file which will be produced as output
    include_bbl:    (bool)  if True the bibliography is included
    noline:         (bool)  avoid newline after merging files
    tex_folder:     (str)   use specific .tex folder
    """
    current_path = os.path.split(base_file)[0]
    with open(output_file, "w") as file_to_write:
        file_to_write.write(''.join(
            expand_file(
                base_file, current_path, include_bbl,
                noline, tex_folder, interactive)))
    return None
