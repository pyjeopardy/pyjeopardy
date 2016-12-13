#!/usr/bin/python3

import os
import shutil
import subprocess
import sys
import tempfile

# set path for import below
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from pyjeopardy.config import COLORS

TEMPLATE = "\\cardfront{{{}}}{{{}}}{{{}}}{{{}}} \\\\[1cm]\n"

def rgb_to_hex(rgb):
    return "{0:02x}{1:02x}{2:02x}".format(*rgb)

def main():
    tmpdir = tempfile.TemporaryDirectory()

    # copy template
    shutil.copy(os.path.join(BASE_DIR, 'placecards', 'template.tex'),
                tmpdir.name)

    # create data file
    with open(os.path.join(tmpdir.name, 'tmpdata.tex'), 'w') as f:
        counter = 0
        for col in COLORS:
            counter += 1
            f.write(TEMPLATE.format(counter, rgb_to_hex(col.rgb()),
                                    rgb_to_hex(col.textcolor_rgb()),
                                    col.name))

    # latex
    tempate_file = os.path.join(tmpdir.name, 'template.tex')
    try:
        subprocess.check_output(["pdflatex", "-halt-on-error",
                                 "-output-directory", tmpdir.name,
                                 tempate_file])
    except subprocess.CalledProcessError as e:
        print(e.output.decode('utf8'))
        sys.exit(1)

    # copy result back
    shutil.copy(os.path.join(tmpdir.name, 'template.pdf'),
                os.path.join(BASE_DIR, 'placecards', 'cards.pdf'))

if __name__ == "__main__":
    main()
