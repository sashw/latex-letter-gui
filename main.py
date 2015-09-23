#!/usr/bin/env python

import sys, os
from letter.letter import Letter

from letter_ui import Ui_MainWindow as gui


#TODO: save/create button filedialog öffnen http://doc.qt.io/qt-5/qfiledialog.html

with Letter() as letter:
    letter.set_absender("John Doe", "Straße der Freiheit", "Berlin")
    text = "This is a line with a lot of symbols in it: % & _ § € ~ ^ \ | £ ° ™ © ¡ äß?\\\n"
    text = letter.replace_symbols_latex(text)
    letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Text bla blub.\n", text, "\end{g-brief}\n", "\end{document}\n"])
    letter.save_tex('test_out.tex')
    letter.create_pdf()
sys.exit(0)


'''
f = tmp_file()
f.write(b"\documentclass{article}\n")
f.write(b"\\usepackage[utf8]{inputenc}\n")
f.write(b"\\usepackage[ngerman]{babel}\n")
f.write(b"\\usepackage{gensymb}\n")
f.write(b"\\usepackage{eurosym}\n")
f.write(b"\\begin{document}\n")
f.write(b"Hello, world!\\\\\n")
text = "This is a line with a lot of symbols in it: % & _ § € ~ ^ \ | £ ° ™ © ¡ äß?\n"
text = replace_symbols_latex(text)
f.write(text.encode('utf-8'))
f.write(b"\end{document}")
f.seek(0)
print(f.read().decode('utf-8'))
'''


from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow
# example: https://misperious.wordpress.com/2014/08/17/python-pyqt5-example/
#TODO: check what really needs to be imported

class MainWindow(QMainWindow, gui):
    def __init__(self, parent=None):
        #QMainWindow.__init__(self, parent)
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())

#TODO: maybe include something like pdf.is_available() to check if latex is installed and can be used  (http://pythonhosted.org/latex/)
#if not pdf.is_available(): ...

'''
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
'''

sys.exit()
