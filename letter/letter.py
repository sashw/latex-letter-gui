# -*- coding: utf-8 -*-

import sys, os
from collections import OrderedDict
from tempfile import TemporaryFile as tmp_file

try:
    from latex import build_pdf, LatexBuildError
except ImportError:
    print("The package 'latex' for Python is not available!")
    print("Please make sure to install it: pip install latex")
    print("with enough rights to install something.")
    sys.exit(1)

class Letter:
    def __init__(self):
        self.__tex = None

        self.__data = OrderedDict([
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

    def _set_val(self, name, val, idx=1):
        self.__data[name][idx] = val

    def set_lochermarke(self, val):
        self._set_val('lochermarke', val)

    def set_faltmarken(self, val):
        self._set_val('faltmarken', val)

    def set_fenstermarken(self, val):
        self._set_val('fenstermarken', val)

    def set_trennlienen(self, val):
        self._set_val('trennlienen', val)

    def set_klassisch(self, val):
        self._set_val('klassisch', val)

    def set_unserzeichen(self, val):
        self._set_val('unserzeichen', val)

    def set_absender(self, name, strasse, ort, land='', zusatz='', retour=''):
        self._set_val('name', name)
        self._set_val('strasse', strasse)
        self._set_val('ort', ort)
        self._set_val('land', land)
        self._set_val('zusatz', zusatz)
        self._set_val('retouradresse', retour)

    def set_ihrschreiben(self, datum):
        self._set_val('ihrschreiben', datum)

    def set_zeichen(self, ihrzeichen, meinzeichen):
        self._set_val('ihrzeichen', ihrzeichen)
        self._set_val('meinzeichen', meinzeichen)

    def set_bank(self, bank, blz, konto):
        self._set_val('bank', bank)
        self._set_val('blz', blz)
        self._set_val('konto', konto)

    def set_tel(self, telefon, telefax='', telex=''):
        self._set_val('telefon', telefon)
        self._set_val('telefax', telefax)
        self._set_val('telex', telex)

    def set_mail(self, mail):
        self._set_val('email', mail)

    def set_homepage(self, web):
        self._set_val('http', web)

    def set_vermerk(self, vermerk):
        self._set_val('postvermerk', vermerk)

    def set_adresse(self, adresse):
        self._set_val('adresse', adresse)

    def set_betreff(self, betreff):
        self._set_val('betreff', betreff)

    def set_anrede(self, anrede):
        self._set_val('anrede', anrede)

    def set_gruss(self, gruss):
        self._set_val('gruss', gruss)

    def set_unterschrift(self, unterschrift):
        self._set_val('unterschrift', unterschrift)

    def set_anlagen(self, anlagen):
        self._set_val('anlagen', anlagen)

    def set_verteiler(self, verteiler):
        self._set_val('verteiler', verteiler)

    def set_text(self, text):
        self._set_val('text', text)

    def _create_tex(self):
        if self.__tex is not None:
            self.__tex.close()

        self.__tex = tmp_file()

        preamble = ['\documentclass[11pt]{g-brief}\n',
                '\\usepackage[utf8]{inputenc}\n',
                '\\usepackage[ngerman]{babel}\n',
                '\\usepackage{enumerate}\n',
                '\\usepackage{gensymb}\n',
                '\\usepackage{eurosym}\n\n']

        self.__tex.writelines(l.encode('utf-8') for l in preamble)
        #for line in preamble:
        #    self.tex.write(line.encode('utf-8'))

        for values in self.__data.values():
            if type(values[1]) is list:
                self.__tex.writelines(line.encode('utf-8') for line in values[1])
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
                self.__tex.write(line.encode('utf-8'))
        self.__tex.write('\endinput'.encode('utf-8'))

    def save_tex(self, filename):
        if not self.__tex:
            self._create_tex()
        self.__tex.seek(0)
        lines = self.__tex.readlines()
        # check if the path exists, if not create the base directory
        basedir = os.path.dirname(filename)
        if basedir and not os.path.exists(basedir):
            os.makedirs(basedir)
        with open(filename, 'w') as f:
            f.writelines(line.decode('utf-8') for line in lines)

    def create_pdf(self, filename=''):
        if not self.__tex:
            self._create_tex()
        if not filename:
            filename = 'letter.pdf'
        self.__tex.seek(0)
        pdf = build_pdf(self.__tex.read().decode('utf-8'))
        pdf.save_to(filename)

    def replace_symbols_latex(self, text):
        replace = {
                '%': '\%',
                '$': '\$',
                '{': '\{',
                '}': '\}',
                '_': '\_',
                '&': '\&',
                '#': '\#',
                '§': '\S',
                '€': '\euro',
                '~': '\\textasciitilde',
                '^': '\\textasciicircum',
                '|': '\\textbar',
                '°': '\degree',
                '<': '\\textless',
                '>': '\\textgreater',
                '£': '\pounds',
                '™': '\\texttrademark',
                '©': '\copyright',
                '®': '\\textregistered',
                '†': '\dag',
                '‡': '\ddag',
                '¶': '\P',
                '¿': '\\textquestiondown',
                '¡': '\\textexclamdown'
                }

        # first replace all backslashes that this won't mess up already replaced symbols
        text = text.replace('\\', '\\textbackslash')
        # and now replace symbols which will mess up the latex compilation
        for i, j in replace.items():
            text = text.replace(i, j)
        return text

