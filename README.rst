================
Latex Letter GUI
================

.. image:: https://travis-ci.org/sashw/latex-letter-gui.svg
    :target: https://travis-ci.org/sashw/latex-letter-gui
    :alt: Travis CI build status (Linux)

.. image:: https://coveralls.io/repos/sashw/latex-letter-gui/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/sashw/latex-letter-gui?branch=master
    :alt: Code Coverage Coveralls

.. image:: http://codecov.io/github/sashw/latex-letter-gui/coverage.svg?branch=master
    :target: http://codecov.io/github/sashw/latex-letter-gui?branch=master
    :alt: Code Coverage Codecov

.. image:: https://img.shields.io/badge/license-GPLv3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License GPLv3

This program provides an easy to use GUI using Qt5 Python bindings in order to create letters with Latex.
Therefore a Letter class is provided which handles the content of the letter as well as creates tex and PDF files.


Requirements
------------

In order to create PDF files, you need to have a Tex distribution like TeX Live installed.

You need to have the Python3 Qt5 bindings installed, ``python-pyqt5`` or ``python3-pyqt5`` depending on your Linux distribution.

On Ubuntu, you can install it with
``sudo apt-get install python3-pyqt5``

Windows
^^^^^^^
If you're running Windows, make sure to install a Tex distribution like TeX Live or MikTeX as well as PyQt5 for your installed Python version. PyQt5 can be downloaded `here <https://riverbankcomputing.com/software/pyqt/download5>`_.

License
-------

This project is licensed under the `GNU General Public License v3.0 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.
