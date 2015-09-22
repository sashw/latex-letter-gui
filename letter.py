import sys, os
from collections import OrderedDict
from tempfile import TemporaryFile as tmp_file

__version__ = 0.3

try:
    from latex import build_pdf, LatexBuildError
except ImportError:
    print("The package 'latex' for Python is not available!")
    print("Please make sure to install it: pip install latex")
    print("with enough rights to install something.")
    sys.exit(1)


class Letter:
    def __init__(self):
        self.tex = None

        self.data = OrderedDict([
            # allgemeine Einstellungen
            ('lochermarke', ['\lochermarke', True]),
            ('faltmarken', ['\\faltmarken', True]),
            ('fenstermarken', ['\\fenstermarken', True]),
            ('trennlinien', ['\\trennlinien', True]),
            ('klassisch', ['\klassisch', False]),
            ('unserzeichen', ['\\unserzeichen', False]),
            # Korrespondenz
            ('ihrzeichen', ['\IhrZeichen', '']),
            ('ihrschreiben', ['\IhrSchreiben', '']),
            ('meinzeichen', ['\MeinZeichen', '']),

            # Absender-Adresse
            ('name', ['\\Name', '']),
            ('strasse', ['\Strasse', '']),
            ('zusatz', ['\Zusatz', '']),
            ('retouradresse', ['\RetourAdresse', '']),
            ('ort', ['\Ort', '']),
            ('land', ['\Land', '']),
            # Kontaktinformationen
            ('telefon', ['\Telefon', '']),
            ('telefax', ['\Telefax', '']),
            ('telex', ['\Telex', '']),
            ('http', ['\HTTP', '']),
            ('email', ['\EMail', '']),
            # Bankverbindung
            ('bank', ['\Bank', '']),
            ('blz', ['\BLZ', '']),
            ('konto', ['\Konto', '']),
            # Anschrift
            ('postvermerk', ['\Postvermerk', '']),
            ('adresse', ['\Adresse', '']),
            # Inhaltsbezogen
            ('datum', ['\Datum', '']),
            ('betreff', ['\Betreff', '']),
            ('anrede', ['\Anrede', '']),
            ('gruss', ['\Gruss', '']),
            ('unterschrift', ['\\Unterschrift', '']),

            ('anlagen', ['\Anlagen', []]),
            ('verteiler', ['\Verteiler', '']),

            # eigentlicher Brieftext, begin document
            ('text', ['text', []]),
            ])

    def set_val(self, name, val, idx=1):
        self.data[name][idx] = val

    def set_lochermarke(self, val):
        self.set_val('lochermarke', val)

    def set_faltmarken(self, val):
        self.set_val('faltmarken', val)

    def set_fenstermarken(self, val):
        self.set_val('fenstermarken', val)

    def set_trennlienen(self, val):
        self.set_val('trennlienen', val)

    def set_klassisch(self, val):
        self.set_val('klassisch', val)

    def set_unserzeichen(self, val):
        self.set_val('unserzeichen', val)

    def set_absender(self, name, strasse, ort, land='', zusatz='', retour=''):
        self.set_val('name', name)
        self.set_val('strasse', strasse)
        self.set_val('ort', ort)
        self.set_val('land', land)
        self.set_val('zusatz', zusatz)
        self.set_val('retouradresse', retour)

    def set_ihrschreiben(self, datum):
        self.set_val('ihrschreiben', datum)

    def set_zeichen(self, ihrzeichen, meinzeichen):
        self.set_val('ihrzeichen', ihrzeichen)
        self.set_val('meinzeichen', meinzeichen)

    def set_bank(self, bank, blz, konto):
        self.set_val('bank', bank)
        self.set_val('blz', blz)
        self.set_val('konto', konto)

    def set_tel(self, telefon, telefax='', telex=''):
        self.set_val('telefon', telefon)
        self.set_val('telefax', telefax)
        self.set_val('telex', telex)

    def set_mail(self, mail):
        self.set_val('email', mail)

    def set_homepage(self, web):
        self.set_val('http', web)

    def set_vermerk(self, vermerk):
        self.set_val('postvermerk', vermerk)

    def set_adresse(self, adresse):
        self.set_val('adresse', adresse)

    def set_betreff(self, betreff):
        self.set_val('betreff', betreff)

    def set_anrede(self, anrede):
        self.set_val('anrede', anrede)

    def set_gruss(self, gruss):
        self.set_val('gruss', gruss)

    def set_unterschrift(self, unterschrift):
        self.set_val('unterschrift', unterschrift)

    def set_anlagen(self, anlagen):
        self.set_val('anlagen', anlagen)

    def set_verteiler(self, verteiler):
        self.set_val('verteiler', verteiler)

    def set_text(self, text):
        self.set_val('text', text)

    def create_tex(self):
        if self.tex is not None:
            self.tex.close()

        self.tex = tmp_file()

        preamble = ['\documentclass[11pt]{g-brief}\n',
                '\\usepackage[utf8]{inputenc}\n',
                '\\usepackage[ngerman]{babel}\n',
                '\\usepackage{enumerate}\n',
                '\\usepackage{gensymb}\n',
                '\\usepackage{eurosym}\n\n']

        self.tex.writelines(l.encode('utf-8') for l in preamble)
        #for line in preamble:
        #    self.tex.write(line.encode('utf-8'))

        for values in self.data.values():
            if type(values[1]) is list:
                self.tex.writelines(line.encode('utf-8') for line in values[1])
            else:
                line = ''
                if type(values[1]) is bool:
                    if values[1]:
                        line = values[0]
                    else:
                        line = '%' + values[0]
                else:
                    line = '%s{%s}' % tuple(values)
                    if '\Gruss' in values[0]:
                        line += '{1cm}'
                line += '\n'
                self.tex.write(line.encode('utf-8'))
        self.tex.write('\endinput'.encode('utf-8'))

    def create_pdf(self, filename=''):
        if not self.tex:
            self.create_tex()
        if not filename:
            filename = 'letter.pdf'
        self.tex.seek(0)
        pdf = build_pdf(self.tex.read().decode('utf-8'))
        pdf.save_to(filename)


letter = Letter()
letter.set_absender("John Doe", "Straße der Freiheit", "Berlin")
letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Text bla blub.\n", "\end{g-brief}\n", "\end{document}\n"])
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
f.write(b"Hello, world!\n")
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

from letter_ui import Ui_MainWindow as gui

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
