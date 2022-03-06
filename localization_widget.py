# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, Qt


class Ui_Localization(object):
    def setupUi(self, Localization):
        Localization.setObjectName("Localization")

        #  Localization.resize(500, 150)
        Localization.setFixedSize(500, 150)
        # Localization.setWindowFlags(Qt.WindowCloseButtonHint )
        self.label = QtWidgets.QLabel(Localization)
        self.label.setGeometry(QtCore.QRect(100, 50, 120, 30))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Localization)
        self.comboBox.setGeometry(QtCore.QRect(230, 50, 120, 40))
        self.comboBox.setObjectName("comboBox")
        # self.comboBox.addItem("")
        # self.comboBox.addItem("en-fr")
        options = ([('English', ''), ('French', 'en-fr'), ])  # ('中文', 'eng-chs'), ])
        for i, (text, lang) in enumerate(options):
            self.comboBox.addItem(text)
            self.comboBox.setItemData(i, lang)

        self.retranslateUi(Localization)
        QtCore.QMetaObject.connectSlotsByName(Localization)

    def retranslateUi(self, Localization):
        _translate = QtCore.QCoreApplication.translate
        Localization.setWindowTitle(_translate("Localization", "Preferences"))
        self.label.setText(_translate("Localization", "Localization"))
        self.comboBox.setItemText(0, _translate("Localization", "English"))
        self.comboBox.setItemText(1, _translate("Localization", "French"))


class Localization(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super(Localization, self).__init__(self.parent)
        self.ui = Ui_Localization()
        self.ui.setupUi(self)

        # self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.trans = QtCore.QTranslator(self)
        self.ui.retranslateUi(self)
        self.ui.comboBox.currentIndexChanged.connect(self.change_func)

    @QtCore.pyqtSlot(int)
    def change_func(self, index):
        data = self.ui.comboBox.itemData(index)
        print("changement")
        print(data)
        if data:
            self.trans.load(data)
            print("load", self.trans.load(data))
            print(self.trans, index)
            print(data)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
            self.ui.comboBox.setItemData(index, self.ui.comboBox.itemData(index))
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
            print("event.type() == QEvent.LanguageChange ==> Ok")
        super(Localization, self).changeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = Localization()
    wind.show()
    sys.exit(app.exec_())
