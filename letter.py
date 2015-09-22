import sys, os
from collections import OrderedDict
from tempfile import TemporaryFile as tmp_file

__version__ = 0.1

try:
    from latex import build_pdf, LatexBuildError
except ImportError:
    print("The package 'latex' for Python is not available!")
    print("Please make sure to install it: pip install latex")
    print("with enough rights to install something.")
    sys.exit(1)


f = tmp_file()
f.write(b"\documentclass{article}\n")
f.write(b"\\usepackage[utf8]{inputenc}\n")
f.write(b"\\usepackage[ngerman]{babel}\n")
f.write(b"\\usepackage{gensymb}\n")
f.write(b"\\usepackage{eurosym}\n")
f.write(b"\\begin{document}\n")
f.write(b"Hello, world!\n")
f.write(b"\end{document}")
f.seek(0)
print(f.read().decode('utf-8'))



#TODO: maybe include something like pdf.is_available() to check if latex is installed and can be used  (http://pythonhosted.org/latex/)
#if not pdf.is_available(): ...

try:
    f.seek(0)
    pdf = build_pdf(f.read().decode('utf-8'))
    pdf.save_to('letter.pdf')
except LatexBuildError as e:
    for error in e.get_errors():
        print(u'Error in {0[filename]}, line {0[line]}: {0[error]}'.format(error))
        # also print one line of context
        print(u'    {}'.format(error['context'][1]))
        print()
    sys.exit("Building pdf failed!")

f.close()  # temporary file is automatically deleted here


sys.exit()
