#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "plantuml" into
plant-generated images.
Needs `plantuml.jar` from http://plantuml.com/.
"""

import os
import sys
import subprocess

from pandocfilters import toJSONFilter, Para, Image
from pandocfilters import get_filename4code, get_caption, get_extension
from dosya import *

PLANTUML_BIN = os.environ.get('PLANTUML_BIN', 'plantuml')
# imageFolder = "deneme"
# def imageFolder(folder:Klasor):
    # return folder

def plantuml(key, value, format_,_):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value
        # print(value)
        # print("caga")
        sys.stderr.write(str(ident))

        if "plantuml" in classes:
            caption, typef, keyvals = get_caption(keyvals)
            imageFolder=Klasor("den/plantuml")
            filename = get_filename4code('DenemeProje2/web/static/Converted_Pdf', code)
            filetype = get_extension(format_, "png", html="svg", latex="png")
            

            src = filename + '.uml'
            dest = filename + '.' + filetype
            # print(src)

            # Generate image only once
            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                if not txt.startswith(b"@start"):
                    txt = b"@startuml\n" + txt + b"\n@enduml\n"
                with open(src, "wb") as f:
                    f.write(txt)

                subprocess.check_call(PLANTUML_BIN.split() +
                                      ["-t" + filetype, src])
                sys.stderr.write('Created image ' + dest + '\n')

            # Update symlink each run
            for ind, keyval in enumerate(keyvals):
                if keyval[0] == 'plantuml-filename':
                    link = keyval[1]
                    keyvals.pop(ind)
                    if os.path.islink(link):
                        os.remove(link)

                    os.symlink(dest, link)
                    dest = link
                    break

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])


def main():
    toJSONFilter(plantuml)


if __name__ == "__main__":
    main()
