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

    # Define __enter__ and __exit__ methods to use Letter with the 'with' statement
    # as a context manager. Use exit to only close the temporary file, no exception
    # handling (if exc_stuff is not None), therefore return nothing like True
    def __enter__(self):
        if not self.__tex:
            self._create_tex()
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        if self.__tex:
            self.__tex.close()  # close temp file to delete it
            self.__tex = None

    def _set_val(self, name, val, idx=1):
        self.__data[name][idx] = val

    def _get_val(self, name, idx=1):
        return self.__data[name][idx]

    def set_lochermarke(self, val):
        self._set_val('lochermarke', val)

    def set_faltmarken(self, val):
        self._set_val('faltmarken', val)

    def set_fenstermarken(self, val):
        self._set_val('fenstermarken', val)

    def set_trennlinien(self, val):
        self._set_val('trennlinien', val)

    def set_klassisch(self, val):
        self._set_val('klassisch', val)

    def set_unserzeichen(self, val):
        self._set_val('unserzeichen', val)

    def set_name(self, name):
        self._set_val('name', name)

    def set_strasse(self, strasse):
        self._set_val('strasse', strasse)

    def set_ort(self, ort):
        self._set_val('ort', ort)

    def set_land(self, land):
        self._set_val('land', land)

    def set_zusatz(self, zusatz):
        self._set_val('zusatz', zusatz)

    def set_retour(self, retour):
        self._set_val('retouradresse', retour)

    def set_absender(self, name, strasse, ort, land='', zusatz='', retour=''):
        self.set_name(name)
        self.set_strasse(strasse)
        self.set_ort(ort)
        self.set_land(land)
        self.set_zusatz(zusatz)
        self.set_retour(retour)

    def get_name(self):
        return self._get_val('name')

    def get_stasse(self):
        return self._get_val('strasse')

    def get_ort(self):
        return self._get_val('ort')

    def get_land(self):
        return self._get_val('land')

    def get_zusatz(self):
        return self._get_val('zusatz')

    def get_retour(self):
        return self._get_val('retouradresse')

    def get_absender(self):
        return (self.get_name(), self.get_stasse(), self.get_ort(), self.get_land(), self.get_zusatz(), self.get_retour())

    def set_ihrschreiben(self, datum):
        self._set_val('ihrschreiben', datum)

    def get_ihrschreiben(self):
        return self._get_val('ihrschreiben')

    def set_zeichen(self, ihrzeichen, meinzeichen):
        self._set_val('ihrzeichen', ihrzeichen)
        self._set_val('meinzeichen', meinzeichen)

    def get_zeichen(self):
        return (self._get_val('ihrzeichen'), self._get_val('meinzeichen'))

    def set_bank_name(self, bank):
        self._set_val('bank', bank)

    def set_blz(self, blz):
        self._set_val('blz', blz)

    def set_konto(self, konto):
        self._set_val('konto', konto)

    def set_bank(self, bank, blz, konto):
        self.set_bank_name(bank)
        self.set_blz(blz)
        self.set_konto(konto)

    def get_bank_name(self):
        return self._get_val('bank')

    def get_blz(self):
        return self._get_val('blz')

    def get_konto(self):
        return self._get_val('konto')

    def get_bank(self):
        return (self.get_bank_name(), self.get_blz(), self.get_konto())

    def set_phone(self, telefon):
        self._set_val('telefon', telefon)

    def set_fax(self, fax):
        self._set_val('telefax', fax)

    def set_telex(self, telex):
        self._set_val('telex', telex)

    def set_tel(self, telefon, telefax='', telex=''):
        self.set_phone(telefon)
        self.set_fax(telefax)
        self.set_telex(telex)

    def get_phone(self):
        return self._get_val('telefon')

    def get_fax(self):
        return self._get_val('telefax')

    def get_telex(self):
        return self._get_val('telex')

    def get_tel(self):
        return (self.get_phone(), self.get_fax(), self.get_telex())

    def set_mail(self, mail):
        self._set_val('email', mail)

    def get_mail(self):
        return self._get_val('email')

    def set_homepage(self, web):
        self._set_val('http', web)

    def get_homepage(self):
        return self._get_val('http')

    def set_vermerk(self, vermerk):
        self._set_val('postvermerk', vermerk)

    def get_vermerk(self):
        return self._get_val('postvermerk')

    def set_adresse(self, adresse):
        self._set_val('adresse', adresse)

    def get_adresse(self):
        return self._get_val('adresse')

    def set_datum(self, datum):
        self._set_val('datum', datum)

    def get_datum(self):
        return self._get_val('datum')

    def set_betreff(self, betreff):
        self._set_val('betreff', betreff)

    def get_betreff(self):
        return self._get_val('betreff')

    def set_anrede(self, anrede):
        self._set_val('anrede', anrede)

    def get_anrede(self):
        return self._get_val('anrede')

    def set_gruss(self, gruss):
        self._set_val('gruss', gruss)

    def get_gruss(self):
        return self._get_val('gruss')

    def set_unterschrift(self, unterschrift):
        self._set_val('unterschrift', unterschrift)

    def get_unterschrift(self):
        return self._get_val('unterschrift')

    def set_anlagen(self, anlagen):
        self._set_val('anlagen', anlagen)

    def get_anlagen(self):
        return self._get_val('anlagen')

    def set_verteiler(self, verteiler):
        self._set_val('verteiler', verteiler)

    def get_verteiler(self):
        return self._get_val('verteiler')

    def set_text(self, text):
        self._set_val('text', text)

    def get_text(self):
        return self._get_val('text')

    def _create_tex(self):
        if self.__tex:
            self.__tex.close()
            self.__tex = None

        self.__tex = tmp_file()

    def _update_tex(self):
        if not self.__tex:
            self._create_tex()

        # delete the content of the temporary file
        self.__tex.seek(0)
        self.__tex.truncate()

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
                if 'text' in values[0]:
                    self.__tex.writelines(line.encode('utf-8') for line in values[1])
                else:
                    line = '%s{\n' % values[0]
                    self.__tex.write(line.encode('utf-8'))
                    self.__tex.writelines(line.encode('utf-8') for line in values[1])
                    self.__tex.write('}\n'.encode('utf-8'))
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

    def _make_tex(self):
        if not self.__tex:
            self._create_tex()
        else:
            self._update_tex()

    def save_tex(self, filename=''):
        self._make_tex()
        if not filename:
            filename = 'letter.tex'

        self.__tex.seek(0)
        lines = self.__tex.readlines()
        # check if the path exists, if not create the base directory
        basedir = os.path.dirname(filename)
        if basedir and not os.path.exists(basedir):
            os.makedirs(basedir)
        with open(filename, 'w') as f:
            f.writelines(line.decode('utf-8') for line in lines)

    def create_pdf(self, filename=''):
        self._make_tex()
        if not filename:
            filename = 'letter.pdf'

        self.__tex.seek(0)
        try:
            pdf = build_pdf(self.__tex.read().decode('utf-8'))
            pdf.save_to(filename)
        except LatexBuildError as e:
            for error in e.get_errors():
                print(u'Error in {0[filename]}, line {0[line]}: {0[error]}'.format(error))
                # also print one line of context
                print(u'    {}'.format(error['context'][1]))
                print()
            self.__tex.close()
            sys.exit("Building PDF failed!")

    def replace_symbols_latex(self, text):
        replace = {
                '%': '\%',
                '$': '\$',
                '{': '\{',
                '}': '\}',
                '_': '\_',
                '&': '\&',
                '#': '\#',
                '§': '\S ',
                '€': '\euro ',
                '~': '\\textasciitilde ',
                '^': '\\textasciicircum ',
                '|': '\\textbar ',
                '°': '\degree ',
                '<': '\\textless ',
                '>': '\\textgreater ',
                '£': '\pounds ',
                '™': '\\texttrademark ',
                '©': '\copyright ',
                '®': '\\textregistered ',
                '†': '\dag ',
                '‡': '\ddag ',
                '¶': '\P ',
                '¿': '\\textquestiondown ',
                '¡': '\\textexclamdown '
                }

        # first replace all backslashes that this won't mess up already replaced symbols
        text = text.replace('\\', '\\textbackslash ')
        # and now replace symbols which will mess up the latex compilation
        for i, j in replace.items():
            text = text.replace(i, j)
        return text

