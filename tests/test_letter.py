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

    def test_tex(self):
        from letter.letter import Letter
        letter = Letter()
        letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Content.\n", "\end{g-brief}\n", "\end{document}\n"])
        ret = letter.save_tex(self.tex)
        self.assertIsNone(ret)

    def test_pdf(self):
        from letter.letter import Letter
        letter = Letter()
        letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Content.\n", "\end{g-brief}\n", "\end{document}\n"])
        ret = letter.create_pdf(self.pdf)
        self.assertIsNone(ret)

    def test_setters(self):
        from letter.letter import Letter
        letter = Letter()
        letter.set_absender("John Doe", "Straße der Freiheit", "Berlin")
        letter.set_adresse("Klaus Störtebeker\\\\Hamburg")
        letter.set_lochermarke(True)
        letter.set_faltmarken(True)
        letter.set_fenstermarken(True)
        letter.set_trennlinien(True)
        letter.set_klassisch(False)
        letter.set_unserzeichen(False)
        letter.set_ihrschreiben("1.1.1970")
        letter.set_zeichen("abc", "xyz")
        letter.set_bank("Top Bank", 12345678, "0123456789")
        letter.set_tel("+00 12345 67890567")
        letter.set_mail("me@mail.tld")
        letter.set_homepage("http://domain.tld")
        letter.set_vermerk("")
        letter.set_datum("21.12.2012")
        letter.set_betreff("Superwichtige Mitteilung")
        letter.set_anrede("Hallo")
        letter.set_gruss("Gruß")
        letter.set_unterschrift("John Doe")
        letter.set_anlagen("")
        letter.set_verteiler("")
        text = "This is a line with a lot of symbols in it: % & _ § € ~ ^ \ | £ ° ™ © ¡ äß?\n"
        text = letter.replace_symbols_latex(text)
        letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Text bla blub.\\\\\n", text, "\end{g-brief}\n", "\end{document}\n"])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

if __name__ == '__main__':
    unittest.main()
