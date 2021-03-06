# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_control_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(281, 252)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.GbMain = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.GbMain.setObjectName("GbMain")
        self.LbControlNum = QtWidgets.QLabel(self.GbMain)
        self.LbControlNum.setGeometry(QtCore.QRect(10, 30, 51, 20))
        self.LbControlNum.setObjectName("LbControlNum")
        self.CbControlNum = QtWidgets.QComboBox(self.GbMain)
        self.CbControlNum.setGeometry(QtCore.QRect(85, 30, 161, 20))
        self.CbControlNum.setCurrentText("")
        self.CbControlNum.setFrame(True)
        self.CbControlNum.setObjectName("CbControlNum")
        self.LbHint = QtWidgets.QLabel(self.GbMain)
        self.LbHint.setGeometry(QtCore.QRect(40, 50, 186, 13))
        self.LbHint.setObjectName("LbHint")
        self.line = QtWidgets.QFrame(self.GbMain)
        self.line.setGeometry(QtCore.QRect(10, 70, 239, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.LbType = QtWidgets.QLabel(self.GbMain)
        self.LbType.setGeometry(QtCore.QRect(10, 80, 24, 20))
        self.LbType.setObjectName("LbType")
        self.LbFunction = QtWidgets.QLabel(self.GbMain)
        self.LbFunction.setGeometry(QtCore.QRect(10, 110, 41, 20))
        self.LbFunction.setObjectName("LbFunction")
        self.LbCommand = QtWidgets.QLabel(self.GbMain)
        self.LbCommand.setGeometry(QtCore.QRect(10, 140, 47, 20))
        self.LbCommand.setObjectName("LbCommand")
        self.LbPort = QtWidgets.QLabel(self.GbMain)
        self.LbPort.setGeometry(QtCore.QRect(10, 170, 20, 20))
        self.LbPort.setObjectName("LbPort")
        self.LeType = QtWidgets.QLineEdit(self.GbMain)
        self.LeType.setEnabled(False)
        self.LeType.setGeometry(QtCore.QRect(80, 80, 171, 20))
        self.LeType.setObjectName("LeType")
        self.CbFunction = QtWidgets.QComboBox(self.GbMain)
        self.CbFunction.setGeometry(QtCore.QRect(80, 110, 171, 20))
        self.CbFunction.setObjectName("CbFunction")
        self.CbFunction.addItem("")
        self.CbFunction.setItemText(0, "change instrument")
        self.CbFunction.addItem("")
        self.CbFunction.setItemText(1, "button")
        self.CbFunction.addItem("")
        self.CbFunction.setItemText(2, "button trigger")
        self.LeCommand = QtWidgets.QLineEdit(self.GbMain)
        self.LeCommand.setGeometry(QtCore.QRect(80, 140, 81, 20))
        self.LeCommand.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferUppercase)
        self.LeCommand.setInputMask("")
        self.LeCommand.setText("")
        self.LeCommand.setObjectName("LeCommand")
        self.LePort = QtWidgets.QLineEdit(self.GbMain)
        self.LePort.setGeometry(QtCore.QRect(80, 170, 81, 20))
        self.LePort.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.LePort.setObjectName("LePort")
        self.LbCommandHint = QtWidgets.QLabel(self.GbMain)
        self.LbCommandHint.setGeometry(QtCore.QRect(180, 140, 47, 13))
        self.LbCommandHint.setObjectName("LbCommandHint")
        self.LbPortHint = QtWidgets.QLabel(self.GbMain)
        self.LbPortHint.setGeometry(QtCore.QRect(180, 170, 47, 13))
        self.LbPortHint.setObjectName("LbPortHint")
        self.verticalLayout.addWidget(self.GbMain)
        self.BbOkCancel = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.BbOkCancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.BbOkCancel.setCenterButtons(False)
        self.BbOkCancel.setObjectName("BbOkCancel")
        self.verticalLayout.addWidget(self.BbOkCancel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.GbMain.setTitle(_translate("Form", "Create new function"))
        self.LbControlNum.setText(_translate("Form", "Control №"))
        self.LbHint.setText(_translate("Form", "Press button or move axe to choose"))
        self.LbType.setText(_translate("Form", "Type"))
        self.LbFunction.setText(_translate("Form", "Function"))
        self.LbCommand.setText(_translate("Form", "Command"))
        self.LbPort.setText(_translate("Form", "Port"))
        self.LbCommandHint.setText(_translate("Form", "0...127"))
        self.LbPortHint.setText(_translate("Form", "0...127"))
