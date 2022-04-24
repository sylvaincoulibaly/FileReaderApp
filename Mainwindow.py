# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QAbstractItemView, QHeaderView, QComboBox, QWidget, QVBoxLayout, QSplitter, \
    QHBoxLayout, QPushButton, QTableView, QMenuBar, QStatusBar, QAction, QToolBar, QMenu

import my_navigation_toolbar_2qt
from my_canvas_matplotlib import CanvasMatplotlib


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        self.app_name = "FileAppReader"
        MainWindow.setWindowTitle(self.app_name)
        MainWindow.setWindowIcon(QIcon("resources/app_icon.png"))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_central_widget = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_central_widget.setObjectName("horizontalLayout_central_widget")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_left = QWidget(self.splitter)
        self.widget_left.setObjectName("widget_left")
        self.verticalLayout = QVBoxLayout(self.widget_left)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_spinbox = QHBoxLayout()
        self.horizontalLayout_spinbox.setObjectName("horizontalLayout_spinbox")
        self.spinBox_x = SpinBox(self.widget_left)  # QtWidgets.QSpinBox(self.widget_left)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_x.sizePolicy().hasHeightForWidth())
        self.spinBox_x.setSizePolicy(sizePolicy)
        self.spinBox_x.setMinimumSize(QtCore.QSize(180, 40))
        self.spinBox_x.setMaximumSize(QtCore.QSize(180, 40))
        self.spinBox_x.setStyleSheet("QSpinBox { border: 1px solid blue;\n"
                                     "                                gridline-color: blue;\n"
                                     "                                border-radius: 2px;\n"
                                     "                                border-style: solid;\n"
                                     "                                background-color: #EEF6FC; \n"
                                     "                                selection-background-color: #218ede;\n"
                                     "                                font-family: Helvetica\n"
                                     "\n"
                                     "                   }")
        # self.spinBox_x.setMaximum(9999)
        self.spinBox_x.setRange(1, 999999)
        self.spinBox_x.setProperty("value", 0)
        self.spinBox_x.setObjectName("spinBox_x")
        # self.spinBox_x.setPrefix(" x - column :  ")
        # self.spinBox_x.setSuffix("\t")
        # self.spinBox_x.setEnabled(False)
        self.horizontalLayout_spinbox.addWidget(self.spinBox_x)

        self.spinBox_y = SpinBox(self.widget_left)  # QtWidgets.QSpinBox(self.widget_left)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_y.sizePolicy().hasHeightForWidth())
        self.spinBox_y.setSizePolicy(sizePolicy)
        self.spinBox_y.setMinimumSize(QtCore.QSize(180, 40))
        self.spinBox_y.setMaximumSize(QtCore.QSize(180, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.spinBox_y.setFont(font)
        self.spinBox_y.setStyleSheet("QSpinBox { border: 1px solid blue;\n"
                                     "                                gridline-color: blue;\n"
                                     "                                border-radius: 2px;\n"
                                     "                                border-style: solid;\n"
                                     "                                background-color: #EEF6FC; \n"
                                     "                                selection-background-color: #218ede;\n"
                                     "                                font-family: Helvetica\n"
                                     "\n"
                                     "                   }")
        self.spinBox_y.setPrefix("")
        # self.spinBox_y.setMaximum(9999)
        self.spinBox_y.setRange(1, 999999)
        self.spinBox_y.setValue(2)

        self.spinBox_y.setObjectName("spinBox_y")
        # self.spinBox_y.setPrefix(" y - column :  ")
        # self.spinBox_y.setEnabled(False)

        self.horizontalLayout_spinbox.addWidget(self.spinBox_y)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_spinbox.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_spinbox)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QComboBox(self.widget_left)
        self.list_sep = {'Semicolon': ';', 'Comma': ',', 'Character tabulation': '\t', 'Space': ' '}
        for cle, valeur in self.list_sep.items():
            self.comboBox.addItems(['{}'.format(cle)])
        self.comboBox.adjustSize()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(370, 40))
        self.comboBox.setMaximumSize(QtCore.QSize(250, 40))
        self.comboBox.setStyleSheet(" QComboBox { border: 1px solid Blue;\n"
                                    "                                gridline-color: blue;\n"
                                    "                                border-radius: 2px;\n"
                                    "                                border-style: solid;\n"
                                    "                                background-color: #EEF6FC; \n"
                                    "                                selection-background-color: #218ede;\n"
                                    "                                font-size: 11.5px;\n"
                                    "                                font-family: Helvetica\n"
                                    "\n"
                                    "                   }")
        self.comboBox.setObjectName("comboBox")
        # self.comboBox.addItem("")
        # self.comboBox.addItem("")
        # self.comboBox.addItem("")
        # self.comboBox.addItem("")
        self.comboBox.blockSignals(False)
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(88, 26, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        btn_size = QSize(30, 30)
        self.btn_add = QPushButton(self.widget_left)
        # self.btn_add.setMaximumSize(QSize(30, 30))
        self.btn_add.setObjectName("btn_add")
        icon_btn_add = QtGui.QIcon()
        icon_btn_add.addPixmap(
            QtGui.QPixmap("resources/gtk_add.png"))
        self.btn_add.setIcon(icon_btn_add)
        self.btn_add.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_add)
        self.btn_delete = QPushButton(self.widget_left)
        #  self.btn_delete.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete.setObjectName("btn_delete")
        icon_btn_delete = QtGui.QIcon()
        icon_btn_delete.addPixmap(
            QtGui.QPixmap("resources/gtk-remove.png"))
        self.btn_delete.setIcon(icon_btn_delete)
        self.btn_delete.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_delete)
        self.btn_sort_x_asc = QPushButton(self.widget_left)
        # self.btn_sort_asc.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_sort_x_asc.setObjectName("btn_sort_asc")
        icon_btn_sort_x_asc = QtGui.QIcon()
        icon_btn_sort_x_asc.addPixmap(
            QtGui.QPixmap("resources/gtk-sort-ascending.png"))
        self.btn_sort_x_asc.setIcon(icon_btn_sort_x_asc)
        self.btn_sort_x_asc.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_sort_x_asc)

        self.btn_sort_x_desc = QPushButton(self.widget_left)
        # self.btn_sort_desc.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_sort_x_desc.setObjectName("btn_sort_desc")
        icon_btn_sort_x_desc = QtGui.QIcon()
        icon_btn_sort_x_desc.addPixmap(
            QtGui.QPixmap("resources/gtk-sort-descending.png"))
        self.btn_sort_x_desc.setIcon(icon_btn_sort_x_desc)
        self.btn_sort_x_desc.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_sort_x_desc)

        self.btn_sort_y_asc = QPushButton(self.widget_left)
        self.btn_sort_y_asc.setObjectName("btn_sort_asc")
        icon_btn_sort_y_asc = QtGui.QIcon()
        icon_btn_sort_y_asc.addPixmap(
            QtGui.QPixmap("resources/gtk-sort-ascending.png"))
        self.btn_sort_y_asc.setIcon(icon_btn_sort_y_asc)
        self.btn_sort_y_asc.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_sort_y_asc)
        self.btn_sort_y_desc = QPushButton(self.widget_left)
        self.btn_sort_y_desc.setObjectName("btn_sort_asc")
        icon_btn_sort_y_desc = QtGui.QIcon()
        icon_btn_sort_y_desc.addPixmap(
            QtGui.QPixmap("resources/gtk-sort-descending.png"))
        self.btn_sort_y_desc.setIcon(icon_btn_sort_y_desc)
        self.btn_sort_y_desc.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_sort_y_desc)

        self.btn_move_up = QPushButton(self.widget_left)
        #  self.btn_move_up.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_move_up.setObjectName("btn_move_up")
        icon_btn_move_up = QtGui.QIcon()
        icon_btn_move_up.addPixmap(
            QtGui.QPixmap("resources/up.png"))
        self.btn_move_up.setIcon(icon_btn_move_up)
        self.btn_move_up.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_move_up)
        self.btn_move_down = QPushButton(self.widget_left)
        #  self.btn_move_down.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_move_down.setObjectName("btn_move_down")
        icon_btn_move_down = QtGui.QIcon()
        icon_btn_move_down.addPixmap(
            QtGui.QPixmap("resources/down.png"))
        self.btn_move_down.setIcon(icon_btn_move_down)
        self.btn_move_down.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_move_down)

        self.btn_copy = QPushButton(self.widget_left)
        self.btn_copy.setObjectName("btn_copy")
        icon_btn_copy = QtGui.QIcon()
        icon_btn_copy.addPixmap(
            QtGui.QPixmap("resources/gtk-copy.png"))
        self.btn_copy.setIcon(icon_btn_copy)
        self.btn_copy.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_copy)

        self.btn_paste = QPushButton(self.widget_left)
        # self.btn_paste.setStyleSheet("    QPushButton { border: 1px solid darkGray;\n"
        #                            "                                gridline-color: blue;\n"
        #                            "                                border-radius: 2px;\n"
        #                            "                                border-style: solid;\n"
        #                            "                                background-color: #EAF6FC; \n"
        #                            "                                selection-background-color: #218ede;\n"
        #                            "                                font-size: 30px;\n"
        #                            "                                font-family: Helvetica\n"
        #                            "\n"
        #                            "                   }")
        self.btn_paste.setObjectName("btn_paste")
        icon_btn_paste = QtGui.QIcon()
        icon_btn_paste.addPixmap(
            QtGui.QPixmap("resources/gtk-paste.png"))
        self.btn_paste.setIcon(icon_btn_paste)
        self.btn_paste.setIconSize(btn_size)
        self.horizontalLayout_4.addWidget(self.btn_paste)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableView = QTableView(self.widget_left)
        self.tableView.setMinimumSize(QtCore.QSize(370, 0))
        # self.tableView.setMaximumSize(QtCore.QSize(370, 1999999))
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # permet de sélectionner une ligne entière
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # ajuster la largeur du tableau
        self.tableView.setAlternatingRowColors(True)  # colorie une ligne sur 2

        font = QtGui.QFont()
        font.setPointSize(14)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.tableView.setStyleSheet(" QTableView { border: 2px solid blue;\n"
                                     "                                gridline-color: blue;\n"
                                     "                                border-radius: 2px;\n"
                                     "                                border-style: solid;\n"
                                     "                                background-color: #EEF6FC; \n"
                                     "                                selection-background-color: #218ede;\n"
                                     "                                font-size: 18px;\n"
                                     "                                font-family: Helvetica\n"
                                     "\n"
                                     "                   }")
        self.verticalLayout.addWidget(self.tableView)

        # self.btn_plot = QtWidgets.QPushButton(self.widget_left)
        # self.btn_plot.setObjectName("btn_paste")
        # icon_btn_plot = QtGui.QIcon()
        # icon_btn_plot.addPixmap(
        #     QtGui.QPixmap("ressources/geometrie_80.png"))
        # self.btn_plot.setIcon(icon_btn_plot)
        # self.btn_plot.setIconSize(btn_size)
        # self.verticalLayout.addWidget(self.btn_plot, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        self.widget_rigth = QWidget(self.splitter)
        self.widget_rigth.setObjectName("widget_right")
        self.verticalLayout_2 = QVBoxLayout(self.widget_rigth)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.texte = QLineEdit(  # "   'Ctrl + click' : Select a point"
        )
        self.texte.setReadOnly(True)
        self.texte.setStyleSheet('''
                           QLineEdit { border: 1px solid darkGray;
                                        gridline-color: blue;
                                        border-radius: 8px;
                                        border-style: solid;
                                        background-color: #EEF6FC; 
                                        selection-background-color: black;
                                        font-size: 19px;
                                        font-family: Helvetica
                           }''')
        self.verticalLayout_2.addWidget(self.texte)
        self.mycanvas = CanvasMatplotlib(width=7, height=10,
                                         dpi=100)  # QtWidgets.QGraphicsView(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(11)

        self.mycanvas.setFont(font)
        self.mycanvas.setObjectName("graphicsView")

        # self.toolbar = MyNavigationToolbar2QT.MyNavigationToolbar2QT(self.mycanvas, self.centralwidget)
        # self.toolbar = NavigationToolbar(self.mycanvas, self.centralwidget)
        self.toolbar = my_navigation_toolbar_2qt.MyNavigationToolbar2QT(self.mycanvas, self.centralwidget)

        self.toolbar.setStyleSheet("QToolBar{ border: 1px solid darkGray;\n"
                                   "                                gridline-color: blue;\n"
                                   "                                border-radius: 4px;\n"
                                   "                                border-style: solid;\n"
                                   "                                background-color: #EEF6FC; \n"
                                   "                                selection-background-color: #218ede;\n"
                                   "                                font-size: 12px;\n"
                                   "                                font-family: Helvetica\n"
                                   "\n"
                                   "                   }")
        #  self.frame_toolbar.addWidget(self.toolbar)
        self.verticalLayout_2.addWidget(self.toolbar)
        self.layout_grahic_param = QtWidgets.QHBoxLayout(self.widget_rigth)
        self.checkbox_isometric_view = QtWidgets.QCheckBox("Isometric view", self.widget_rigth)
        # self.checkbox_isometric_view.setStyleSheet("    QCheckBox { border: 1px solid darkGray;\n"
        #                                            "                                gridline-color: blue;\n"
        #                                            "                                border-radius: 2px;\n"
        #                                            "                                border-style: solid;\n"
        #                                            "                                background-color: #EEF6FC; \n"
        #                                            "selection-background-color: #218ede;\n "
        #                                            "                                font-size: 19px;\n"
        #                                            "                                font-family: Helvetica\n"
        #                                            "\n"
        #                                            "                   }")
        self.layout_grahic_param.addWidget(self.checkbox_isometric_view)
        self.verticalLayout_2.addLayout(self.layout_grahic_param)
        self.verticalLayout_2.addWidget(self.mycanvas)

        self.horizontalLayout_central_widget.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menu_parameter = QMenu(self.menubar)
        # self.actionbtn_preferences = QAction(MainWindow)
        # self.actionbtn_preferences.setText("Preferences")
        # self.actionbtn_preferences.setObjectName("actionbtn_preferences")
        self.menu_parameter.setObjectName("menu_parameter")
        self.menu_parameter.setTitle("Parameters")
        # self.menu_parameter.addAction(self.actionbtn_preferences)

        self.menu_preferences = QMenu(self.menu_parameter)
        self.menu_preferences.setObjectName("menu_preferences")
        self.menu_preferences.setTitle("Preferences")
        self.actionbtn_localization = QAction(MainWindow)
        self.actionbtn_localization.setObjectName("actionbtn_localization")
        self.actionbtn_localization.setText("localization")
        self.menu_preferences.addAction(self.actionbtn_localization)

        self.menu_parameter.addAction(self.menu_preferences.menuAction())
        self.menubar.addAction(self.menu_parameter.menuAction())

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.actionbtn_open = QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/gtk-open.png"), QIcon.Normal, QIcon.On)
        self.actionbtn_open.setIcon(icon)
        self.actionbtn_open.setObjectName("actionbtn_open")
        self.toolBar.addAction(self.actionbtn_open)

        self.actionbtn_save_as = QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/gtk-save-as.png"), QIcon.Normal, QIcon.On)
        self.actionbtn_save_as.setIcon(icon)
        self.actionbtn_save_as.setObjectName("actionbtn_save_as")
        self.toolBar.addAction(self.actionbtn_save_as)
        self.toolBar.setIconSize(QSize(30, 30))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # self.MainWindow = MainWindow
        # self.name_app = "FileReaderApp"
        # self.path_file = ""
        # self.MainWindow.setWindowTitle(f"{self.name_app} {self.path_file}")
        # MainWindow.setWindowTitle(_translate("MainWindow", self.name_app))
        self.menu_parameter.setTitle(_translate("MainWindow", "Parameters"))
        self.menu_preferences.setTitle(_translate("MainWindow", "Preferences"))
        self.actionbtn_localization.setText(_translate("MainWindow", "Localization"))
        self.spinBox_x.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; "
            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
            "text-indent:0px;\"><span style=\" font-size:10pt; "
            "color:#0000ff;\">" +
            _translate("MainWindow", "Indicate the column number corresponding to x") +
            "</span></pre></body></html>")
        self.spinBox_x.setPrefix(_translate("MainWindow", " x - column :  "))

        self.spinBox_y.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; "
            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
            "text-indent:0px;\"><span style=\" font-size:10pt; "
            "color:#0000ff;\">" +
            _translate("MainWindow", "Indicate the column number corresponding to y") +
            "</span></pre></body></html>")
        self.spinBox_y.setPrefix(_translate("MainWindow", " y - column :  "))

        self.comboBox.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; "
            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
            "text-indent:0px;\"><span style=\" font-size:10pt; "
            "color:#0000ff;\">" +
            _translate("MainWindow", "Choose the column separator") +
            "</span></pre></body></html>")

        self.comboBox.setItemText(0, _translate("MainWindow", "Semicolon"))
        #  self.comboBox.addItem(_translate("MainWindow", "Semicolon"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Comma"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Character tabulation"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Space"))

        # self.comboBox.addItem(_translate("MainWindow", "Semicolon"))
        # self.comboBox.addItem(_translate("MainWindow", "Comma"))
        # self.comboBox.addItem(_translate("MainWindow", "Character tabulation"))
        # self.comboBox.addItem(_translate("MainWindow", "Space"))

        # self.list_sep = {'Semicolon': ';', 'Comma': ',', 'Character tabulation': '\t', 'Space': ' '}
        # for cle, valeur in self.list_sep.items():
        #     #self.comboBox.addItems(['{}'.format(cle)])
        #     _translate("MainWindow", str(cle))

        # self.list_sep = {_translate("MainWindow", "Semicolon"): ';', _translate("MainWindow", "Comma"): ',',
        #                  _translate("MainWindow", "Character tabulation"): '\t', _translate("MainWindow","Space"): ' '}
        # for cle, valeur in self.list_sep.items():
        #     self.comboBox.addItems(['{}'.format(cle)])
        #     print(cle)
        # print(self.list_sep)

        # options = ([('English', ''), ('Français', 'eng-fr'), ('中文', 'eng-chs'), ])
        # for i, (text, lang) in enumerate(options):
        #     self.comboBox.addItem(text)
        #     self.comboBox.setItemData(i, lang)

        self.btn_add.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; "
            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
            "text-indent:0px;\"><span style=\" font-size:10pt; color:#0000ff;\">" +
            _translate("MainWindow", "Add row") +
            "</span></pre></body></html>")
        # self.btn_add.setText(_translate("MainWindow", ""))

        self.btn_delete.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; "
            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
            "text-indent:0px;\"><span style=\" font-size:10pt; "
            "color:#0000ff;\">" +
            _translate("MainWindow", "Delete the selected row") +
            "</span></pre></body></html>")
        # self.btn_delete.setText(_translate("MainWindow", ""))

        self.btn_sort_x_asc.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\">" +
            _translate("MainWindow", "Sort by ascending x") +
            "</span></pre></body></html>")
        # self.btn_sort_x_asc.setText(_translate("MainWindow", ""))

        self.btn_sort_x_desc.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\">" +
            _translate("MainWindow", "Sort by descending x") +
            "</span></pre></body></html>")
        # self.btn_sort_x_desc.setText(_translate("MainWindow", ""))

        self.btn_sort_y_asc.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\" >" +
            _translate("MainWindow", "Sort by ascending y") +
            "</span></pre></body></html>")
        # self.btn_sort_y_asc.setText(_translate("MainWindow", ""))

        self.btn_sort_y_desc.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\" >" +
            _translate("MainWindow", "Sort by descending y") +
            "</span></pre></body></html>")
        # self.btn_sort_y_desc.setText(_translate("MainWindow", ""))

        self.btn_move_up.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; margin-bottom:12px; "
            "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
            "text-indent:0px;\"><span style=\" font-size:10pt; "
            "color:#0000ff;\" >" +
            _translate("MainWindow", "Move up selected row") +
            "</span></pre></body></html>")
        # self.btn_move_up.setText(_translate("MainWindow", ""))

        self.btn_move_down.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\" >"
            + _translate("MainWindow", "Move down selected row") +
            "</span></pre></body></html>")
        # self.btn_move_down.setText(_translate("MainWindow", ""))

        self.btn_copy.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\">" +
            _translate("MainWindow", "Copy selected row") +
            "</span></pre></body></html>")
        # self.btn_copy.setText(_translate("MainWindow", ""))

        self.btn_paste.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; color:#0000ff;\">" +
            _translate("MainWindow", "Paste selected row") +
            "</span></pre></body></html>")
        # self.btn_paste.setText(_translate("MainWindow", ""))

        self.texte.setToolTip(
            "<html><head/><body><pre style=\" margin-top:12px; "
            "margin-bottom:12px; margin-left:0px; margin-right:0px; "
            "-qt-block-indent:0; text-indent:0px;\"><span style=\" "
            "font-size:10pt; \">" +
            _translate("MainWindow", "Press the CTRL + CLICK key "
                                     "combination to find the row \nof the table corresponding to the point "
                                     "targeted") +
            "</span></pre></body></html>")
        # self.texte.setText(_translate("MainWindow", "Select a point"))
        self.texte.setText(_translate("MainWindow", "   'Ctrl + click' : Select a point"))
        self.checkbox_isometric_view.setText(_translate("MainWindow", "Isometric view"))

        # self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        # self.actionbtn_open.setText(_translate("MainWindow", "btn_open"))

        self.actionbtn_open.setToolTip(_translate("MainWindow", "Select file (Ctrl+O)"))
        self.actionbtn_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionbtn_save_as.setText(_translate("MainWindow", "btn_save_as"))
        self.actionbtn_save_as.setToolTip(_translate("MainWindow", "Save as file  (Ctrl+S)"))
        self.actionbtn_save_as.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.toolbar.toolitems_translation()  # pour l'internationalisation des tooltip de la toolbar


class SpinBox(QtWidgets.QSpinBox):
    upClicked = QtCore.pyqtSignal()
    downClicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        last_value = self.value()
        super(SpinBox, self).mousePressEvent(event)
        if self.value() < last_value:
            self.downClicked.emit()
        elif self.value() > last_value:
            self.upClicked.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
