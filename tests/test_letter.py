#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_letter
----------------------------------

Tests for `letter` module.
"""

import unittest
from os import remove as rm
from os import getcwd as pwd
from os.path import join as pjoin

from letter.letter import Letter


class TestLetter(unittest.TestCase):

    def setUp(self):
        self.pwd = pwd()
        self.tex = pjoin(self.pwd, 'test_out.tex')
        self.pdf = pjoin(self.pwd, 'test_out.pdf')
        self.letter = Letter()
        self.letter.set_absender("John Doe", "Straße der Freiheit", "Berlin")
        text = "This is a line with a lot of symbols in it: % & _ § € ~ ^ \ | £ ° ™ © ¡ äß?\\\n"
        text = self.letter.replace_symbols_latex(text)
        self.letter.set_text(["\n", "\\begin{document}\n", "\\begin{g-brief}\n", "Text bla blub.\n", text, "\end{g-brief}\n", "\end{document}\n"])

    def test_tex(self):
        ret = self.letter.save_tex(self.tex)
        self.assertIsNone(ret)

    def test_pdf(self):
        ret = self.letter.create_pdf(self.pdf)
        self.assertIsNone(ret)

    def tearDown(self):
        self.letter.__exit__()
        rm(self.tex)
        rm(self.pdf)

if __name__ == '__main__':
    unittest.main()
