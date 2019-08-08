# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(268, 312)
        Dialog.setMinimumSize(QtCore.QSize(268, 312))
        Dialog.setMaximumSize(QtCore.QSize(268, 312))
        self.sign_in_btn = QtWidgets.QPushButton(Dialog)
        self.sign_in_btn.setGeometry(QtCore.QRect(40, 210, 75, 23))
        self.sign_in_btn.setObjectName("sign_in_btn")
        self.sign_up_btn = QtWidgets.QPushButton(Dialog)
        self.sign_up_btn.setGeometry(QtCore.QRect(140, 210, 75, 23))
        self.sign_up_btn.setObjectName("sign_up_btn")
        self.user_name = QtWidgets.QLineEdit(Dialog)
        self.user_name.setGeometry(QtCore.QRect(80, 80, 113, 20))
        self.user_name.setObjectName("user_name")
        self.user_passwd = QtWidgets.QLineEdit(Dialog)
        self.user_passwd.setGeometry(QtCore.QRect(80, 110, 113, 20))
        self.user_passwd.setObjectName("user_passwd")
        # self.user_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 80, 31, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 110, 31, 16))
        self.label_2.setObjectName("label_2")
        self.check_ret = QtWidgets.QLabel(Dialog)
        self.check_ret.setGeometry(QtCore.QRect(80, 140, 161, 16))
        self.check_ret.setText("")
        self.check_ret.setObjectName("check_ret")

        self.retranslateUi(Dialog)
        self.sign_in_btn.clicked.connect(Dialog.sign_in)
        self.sign_up_btn.clicked.connect(Dialog.sign_up)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "login"))
        self.sign_in_btn.setText(_translate("Dialog", "登录"))
        self.sign_up_btn.setText(_translate("Dialog", "注册"))
        self.label.setText(_translate("Dialog", "账号"))
        self.label_2.setText(_translate("Dialog", "密码"))

