#!/usr/bin/env python

import sys, os

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

from letter.letter import Letter
from letter.main_gui import Ui_MainWindow as gui
from letter.bank_gui import Ui_BankDialog as bank

#TODO: maybe include something like pdf.is_available() to check if latex is installed and can be used  (http://pythonhosted.org/latex/)
#if not pdf.is_available(): ...

#TODO: save/create button filedialog öffnen http://doc.qt.io/qt-5/qfiledialog.html

class BankDialog(QDialog, bank):
    def __init__(self, parent=None):
        super(BankDialog, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QMainWindow, gui):
    def __init__(self, parent=None):
        #QMainWindow.__init__(self, parent)
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # set minimum date in calendar widget to 30 days ago
        import datetime
        date = datetime.datetime.now() - datetime.timedelta(days=30)
        min_date = (date.year, date.month, date.day)
        self.calendarWidget.setMinimumDate(QDate(*min_date))

    def set_letter(self, letter):
        self.letter = letter

    def __prepare_line(self, line):
        return self.letter.replace_symbols_latex(line)

    def __prepare_text(self, raw):
        raw = raw.split('\n')
        text = []
        for line in raw:
            line = self.__prepare_line(line)
            line += '\\\\\n'
            text.append(line)
        return text

    def __prepare_content(self, content):
        content = self.__prepare_text(content)
        text = ['\\begin{document}\n', '\\begin{g-brief}\n']
        text += content
        text += ['\end{g-brief}\n', '\end{document}\n']
        return text

    def __collect_values(self):
        missing = []

        self.letter.set_lochermarke(self.lochermarke_checkbox.isChecked())
        self.letter.set_faltmarken(self.faltmarken_checkbox.isChecked())
        self.letter.set_fenstermarken(self.fenstermarken_checkbox.isChecked())
        self.letter.set_trennlinien(self.trennlinien_checkbox.isChecked())

        name = self.name_line.text()
        street = self.street_line.text()
        city = self.city_line.text()
        country = self.country_line.text()
        if not name:
            missing.append(self.name_label)
        if not street:
            missing.append(self.street_label)
        if not city:
            missing.append(self.city_label)
        self.letter.set_absender(name, street, city, country)
        self.letter.set_unterschrift(name)

        recipient = self.recipient_text.toPlainText()
        if not recipient:
            missing.append(self.recipient_label)
        recipient = self.__prepare_text(recipient)
        self.letter.set_adresse(recipient)

        content = self.content_text.toPlainText()
        if not content:
            missing.append(self.content_label)
        text = self.__prepare_content(content)
        self.letter.set_text(text)

        subject = self.subject_line.text()
        if not subject:
            missing.append(self.subject_label)
        subject = self.__prepare_line(subject)
        self.letter.set_betreff(subject)
        salutation = self.salutation_line.text()
        if not salutation:
            missing.append(self.salutation_label)
        salutation = self.__prepare_line(salutation)
        self.letter.set_anrede(salutation)
        greeting = self.greeting_line.text()
        if not greeting:
            missing.append(self.greeting_label)
        greeting = self.__prepare_line(greeting)
        self.letter.set_gruss(greeting)

        mail = self.email_line.text()
        if mail:
            self.letter.set_mail(mail)
        phone = self.phone_line.text()
        if phone:
            self.letter.set_phone(phone)

        date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy")
        if self.only_date_radio.isChecked():
            self.letter.set_datum(date)
        else:
            city = city.partition(' ')[2]
            self.letter.set_datum('%s, %s' % (date, city))

        return missing

    def _check_values(self):
        missing = self.__collect_values()
        if missing:
            print('Missing fields:')
            for miss in missing:
                print(miss.text(), miss.buddy())
            return False
        else:
            return True

    def showBank(self):
        bank, blz, konto, result = self._getBank(self)
        if result:
            self.letter.set_bank(bank, blz, konto)

    def save_tex(self):
        if self._check_values():
            self.letter.save_tex()
            print('letter.tex created')

    def create_pdf(self):
        if self._check_values():
            self.letter.create_pdf()
            print('letter.pdf created')

    # static method to show the bank dialog and get bank name, code, and account
    @staticmethod
    def _getBank(parent=None):
        dialog = BankDialog(parent)
        try:
            if parent.letter and isinstance(parent.letter, Letter):
                bank, blz, konto = parent.letter.get_bank()
                dialog.bank_name_line.setText(bank)
                dialog.bank_code_line.setText(blz)
                dialog.account_line.setText(konto)
        except AttributeError:
            pass
        result = dialog.exec_()
        return (dialog.bank_name_line.text(), dialog.bank_code_line.text(), dialog.account_line.text(), result == QDialog.Accepted)


def main():
    with Letter() as letter:
        app = QApplication(sys.argv)
        w = MainWindow()
        w.set_letter(letter)
        w.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    #except KeyboardInterrupt:
    #    print('\nCtrl+C detected, closing GUI')
    #    sys.exit(0)
    except Exception as exc:
        print('An error occured during execution:')
        print(exc)
        sys.exit(1)

