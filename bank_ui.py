# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bank_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(352, 250)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 190, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 40, 291, 121))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.layout.setObjectName("layout")
        self.labels_layout = QtWidgets.QVBoxLayout()
        self.labels_layout.setObjectName("labels_layout")
        self.bank_name_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.bank_name_label.setObjectName("bank_name_label")
        self.labels_layout.addWidget(self.bank_name_label)
        self.bank_code_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.bank_code_label.setObjectName("bank_code_label")
        self.labels_layout.addWidget(self.bank_code_label)
        self.account_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.account_label.setObjectName("account_label")
        self.labels_layout.addWidget(self.account_label)
        self.layout.addLayout(self.labels_layout)
        self.lines_layout = QtWidgets.QVBoxLayout()
        self.lines_layout.setObjectName("lines_layout")
        self.bank_name_line = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.bank_name_line.setObjectName("bank_name_line")
        self.lines_layout.addWidget(self.bank_name_line)
        self.bank_code_line = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.bank_code_line.setObjectName("bank_code_line")
        self.lines_layout.addWidget(self.bank_code_line)
        self.account_line = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.account_line.setObjectName("account_line")
        self.lines_layout.addWidget(self.account_line)
        self.layout.addLayout(self.lines_layout)
        self.bank_name_label.setBuddy(self.bank_name_line)
        self.bank_code_label.setBuddy(self.bank_code_line)
        self.account_label.setBuddy(self.account_line)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.bank_name_label.setText(_translate("Dialog", "Bank"))
        self.bank_code_label.setText(_translate("Dialog", "BLZ"))
        self.account_label.setText(_translate("Dialog", "Konto"))

