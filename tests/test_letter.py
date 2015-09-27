#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_letter
----------------------------------

Tests for `letter` module.
"""

import unittest
import sys, shutil, tempfile
from os.path import join as pjoin
# use builtins to test ImportError
try:
    import builtins
except ImportError:
    import __builtin__ as builtins


class TestLetter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        cls.tex = pjoin(cls.test_dir, 'some/useless/dirs/test_out.tex')
        cls.pdf = pjoin(cls.test_dir, 'test_out.pdf')

    def test_00_import_error(self):
        # construct a method which let the import of the latex package fail
        self.original_import = builtins.__import__
        def fail_import(name, *args, **kwargs):
            if name is 'latex':
                raise ImportError
            return self.original_import(name, *args, **kwargs)
        builtins.__import__ = fail_import

        with self.assertRaises(SystemExit) as exc:
            from letter.letter import Letter
        self.assertEqual(exc.exception.code, 1)

        builtins.__import__ = self.original_import

    def test_context_manager(self):
        from letter.letter import Letter
        with Letter() as letter:
            pass

    def test_update_empty(self):
        from letter.letter import Letter
        with Letter() as letter:
            letter.__exit__()
            ret = letter._update_tex()
        self.assertIsNone(ret)

    def test_create_make_conditions(self):
        from letter.letter import Letter
        letter = Letter()
        letter._make_tex()
        letter._create_tex()
        letter.__exit__()

    def test_tex(self):
        from letter.letter import Letter
        with Letter() as letter:
            letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Content.\n", "\end{g-brief}\n", "\end{document}\n"])
            ret = letter.save_tex(self.tex)
        self.assertIsNone(ret)

    def test_pdf(self):
        from letter.letter import Letter
        with Letter() as letter:
            letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Content.\n", "\end{g-brief}\n", "\end{document}\n"])
            ret = letter.create_pdf(self.pdf)
        self.assertIsNone(ret)

    def test_tex_pdf_without_filename(self):
        from letter.letter import Letter
        with Letter() as letter:
            letter.set_text(["\\begin{document}\n", "\\begin{g-brief}\n", "\end{g-brief}\n", "\end{document}\n"])
            tex = letter.save_tex()
            pdf = letter.create_pdf()
        self.assertEqual(tex, pdf)
        from os.path import isfile
        self.assertTrue(isfile('letter.tex'))
        self.assertTrue(isfile('letter.pdf'))

    def test_pdf_fail_missing_begin_document(self):
        from letter.letter import Letter
        with Letter() as letter:
            with self.assertRaises(SystemExit) as exc:
                letter.create_pdf(self.pdf)
            self.assertEqual(exc.exception.code, 'Building PDF failed!')

    def test_pdf_fail_syntax(self):
        from letter.letter import Letter
        with Letter() as letter:
            letter.set_text(["\\begin{document}\n", "\\begin{g-brief}\n", "\end{g-brief}\n"])
            with self.assertRaises(SystemExit) as exc:
                letter.create_pdf(self.pdf)
            self.assertEqual(exc.exception.code, 'Building PDF failed!')

    def test_symbol_replace(self):
        from letter.letter import Letter
        with Letter() as letter:
            text = "Lots of symbols: %& _d§ €a~rt^4 \| £ö°o™ß© ¡?"
            replaced = letter.replace_symbols_latex(text)
            self.assertEqual(replaced,
                    'Lots of symbols: \%\& \_d\S  \euro a\\textasciitilde rt\\textasciicircum 4 \\textbackslash \\textbar  \pounds ö\degree o\\texttrademark ß\copyright  \\textexclamdown ?')

    def test_setters_and_getters(self):
        from letter.letter import Letter
        letter = Letter()
        letter.set_absender("John Doe", "Straße der Freiheit", "Berlin")
        absender = letter.get_absender()
        self.assertEqual(("John Doe", "Straße der Freiheit", "Berlin", "", "", ""), absender)
        letter.set_adresse("Klaus Störtebeker\\\\Hamburg")
        self.assertEqual("Klaus Störtebeker\\\\Hamburg", letter.get_adresse())
        letter.set_lochermarke(True)
        letter.set_faltmarken(True)
        letter.set_fenstermarken(True)
        letter.set_trennlinien(True)
        letter.set_klassisch(False)
        letter.set_unserzeichen(False)
        letter.set_ihrschreiben("1.1.1970")
        self.assertEqual("1.1.1970", letter.get_ihrschreiben())
        letter.set_zeichen("abc", "xyz")
        self.assertEqual(("abc", "xyz"), letter.get_zeichen())
        bank = ("Top Bank", 12345678, "0123456789")
        letter.set_bank(*bank)
        get_bank = letter.get_bank()
        self.assertEqual(bank, get_bank)
        letter.set_tel("+00 12345 67890567")
        self.assertEqual(("+00 12345 67890567", '', ''), letter.get_tel())
        letter.set_mail("me@mail.tld")
        self.assertEqual("me@mail.tld", letter.get_mail())
        letter.set_homepage("http://domain.tld")
        self.assertEqual("http://domain.tld", letter.get_homepage())
        letter.set_vermerk("")
        self.assertEqual("", letter.get_vermerk())
        letter.set_datum("21.12.2012")
        self.assertEqual("21.12.2012", letter.get_datum())
        letter.set_betreff("Superwichtige Mitteilung")
        self.assertEqual("Superwichtige Mitteilung", letter.get_betreff())
        letter.set_anrede("Hallo")
        self.assertEqual("Hallo", letter.get_anrede())
        letter.set_gruss("Gruß")
        self.assertEqual("Gruß", letter.get_gruss())
        letter.set_unterschrift("John Doe")
        self.assertEqual("John Doe", letter.get_unterschrift())
        letter.set_anlagen("")
        self.assertEqual("", letter.get_anlagen())
        letter.set_verteiler("")
        self.assertEqual("", letter.get_verteiler())
        text = "This is a line with a lot of symbols in it: % & _ § € ~ ^ \ | £ ° ™ © ¡ äß?\n"
        text = letter.replace_symbols_latex(text)
        letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Text bla blub.\\\\\n", text, "\end{g-brief}\n", "\end{document}\n"])
        self.assertEqual(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Text bla blub.\\\\\n", text, "\end{g-brief}\n", "\end{document}\n"], letter.get_text())
        letter.__exit__()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

if __name__ == '__main__':
    unittest.main()
