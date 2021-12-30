#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  11 13:27:58 2021
@author: Sylvain Coulibaly
"""

import os
import sys
import pathlib

import pandas as pd
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSettings, Qt, QEvent
from PyQt5.QtWidgets import QFileDialog, QApplication

from Mainwindow import Ui_MainWindow
from qtableview_model import PandasModelEditable, Delegate
import mpl_canvas_onpick_event
import message_box


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.filename = None
        self.file_extension = None
        self.x_label = "x"
        self.y_label = "y"
        self.ui.spinBox_x.setEnabled(False)
        self.ui.spinBox_y.setEnabled(False)
        # self.ui.comboBox.setEnabled(False)

        self.model = None
        self.setup_tableview()
        self.setup_connections()
        self.graph()
        if self.model:
            self.model.dataChanged.connect(
                self.graph)  # permet de mettre à jour le graphique lorsqu'on modifie et tape sur la touche ENTREE


    def setup_connections(self):
        self.ui.actionbtn_open.triggered.connect(self.open_file_dialog)
        self.ui.btn_add.clicked.connect(self.insert_row)
        self.ui.btn_delete.clicked.connect(self.delete_row)
        self.ui.btn_sort_x_asc.clicked.connect(self.sort_x_ascending)
        self.ui.btn_sort_x_desc.clicked.connect(self.sort_x_descending)
        self.ui.btn_sort_y_asc.clicked.connect(self.sort_y_ascending)
        self.ui.btn_sort_y_desc.clicked.connect(self.sort_y_descending)
        self.ui.btn_move_up.clicked.connect(self.move_row_up)
        self.ui.btn_move_down.clicked.connect(self.move_row_down)
        self.ui.btn_copy.clicked.connect(self.copy_table)
        self.ui.btn_paste.clicked.connect(self.paste_table)

        self.ui.spinBox_x.upClicked.connect(self.update_tableview)
        self.ui.spinBox_x.downClicked.connect(self.update_tableview)
        self.ui.spinBox_y.upClicked.connect(self.update_tableview)
        self.ui.spinBox_y.downClicked.connect(self.update_tableview)

        self.ui.comboBox.currentTextChanged.connect(self.update_tableview)
        self.ui.checkbox_isometric_view.stateChanged.connect(self.isometric_view)

    def setup_tableview(self):
        self.model = PandasModelEditable(pd.DataFrame({"x": [], "y": []}))
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())
        self.ui.tableView.installEventFilter(self)  # pour les fonctions copier/coller

    def setup_model(self):
        x, y = self.get_data_x_y()
        if self.x_label == self.y_label:
            # ==> pd.DataFrame n'autorise pas une duplication du nom des colonnes
            self.x_label = "{} ".format(self.x_label)
            self.model = PandasModelEditable(pd.DataFrame({self.x_label: x, self.y_label: y}),
                                             table_header=[self.x_label, self.y_label])
        else:
            self.model = PandasModelEditable(pd.DataFrame({self.x_label: x, self.y_label: y}),
                                             table_header=[self.x_label, self.y_label])

        self.ui.tableView.setModel(self.model)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        DEFAULT_DIRECTORY = '/home/'
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'MyOrg', )  # application='MyApp', )
        current_dir = settings.value('current_directory', DEFAULT_DIRECTORY, type=str)
        options |= QFileDialog.DontUseNativeDialog

        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open a file ', current_dir,
                                                       "CSV Files (*.csv);;Text Files (*.txt);;HDF5 Files ("
                                                       "*.h5);;All Files (*)",
                                                       options=options)
        current_dir = os.path.split(self.filename)[0] or DEFAULT_DIRECTORY
        settings.setValue('current_directory', current_dir)
        if self.filename and self.filename != "":
            self.setWindowTitle(self.ui.name_app + " ~ Open file : " + self.filename)
            print("Open file :", self.filename)
            self.ui.spinBox_x.setEnabled(True)
            self.ui.spinBox_y.setEnabled(True)
            # self.ui.comboBox.setEnabled(True)
            self.file_extension = pathlib.Path(self.filename).suffix
            self.setup_model()
            self.graph()
            self.model.dataChanged.connect(self.graph)

    def update_tableview(self):
        if self.filename:
            self.setup_model()
            self.graph()

    def _get_xy_txt_csv(self):
        print(self.ui.comboBox.currentText())
        data_delimiter = self.ui.list_sep['{}'.format(self.ui.comboBox.currentText())]
        df = pd.read_csv(str(self.filename), delimiter=data_delimiter, skipinitialspace=True,
                         doublequote=True,
                         comment='*')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # pour supprimer les colonnes Unnamed
        header_df = list(df.columns)
        "########################################################################################################"
        """ Pour prendre en compte les CSV qui contiennent le séparateur de colonnes à la fin de chaque ligne"""
        df = pd.read_csv(str(self.filename), sep=data_delimiter, skipinitialspace=True, header=0,
                         names=header_df, usecols=range(len(header_df)),  # skip_blank_lines=True,
                         comment='*')  # ,skiprows=1) header=0,
        "########################################################################################################"

        with open(str(self.filename), 'r') as csv_file:
            """ On ouvre le fichier CSV et vérifie après s'il contient le séparateur de colonnes sélectionné """
            header = csv_file.readline()
        print("ùùùù", header)
        print(df)

        if self.ui.spinBox_y.value() <= len(header_df) < self.ui.spinBox_x.value():

            if header.find('{}'.format(data_delimiter)) != -1:
                message_box.message_box_critical_index_error_x_column(self.ui.comboBox, "x")
                self.ui.spinBox_x.setValue(self.ui.spinBox_x.value() - 1)
        if self.ui.spinBox_x.value() <= len(header_df) < self.ui.spinBox_y.value():
            if header.find('{}'.format(data_delimiter)) != -1:
                message_box.message_box_critical_index_error_y_column(self.ui.comboBox)
                self.ui.spinBox_y.setValue(self.ui.spinBox_y.value() - 1)

        if len(header_df) < self.ui.spinBox_x.value() and len(header_df) < self.ui.spinBox_y.value():
            if header.find('{}'.format(data_delimiter)) != -1:
                message_box.message_box_critical_index_error_x_column(self.ui.comboBox, "x")
                message_box.message_box_critical_index_error_y_column(self.ui.comboBox)
        print(header.find('{}'.format(data_delimiter)))
        print(header)
        print("\n", header.split(data_delimiter), header.split(" "), len(header_df), df.shape)
        if header.find('{}'.format(data_delimiter)) != -1 and len(header.split(data_delimiter)) == len(header_df):
            """###########################################"""
            print(header.split(data_delimiter))
            if not (data_delimiter == " " and ["\t" in el for el in header.split(data_delimiter)]):
                """##########################################################################"""
                print("delimiter ", data_delimiter)
                x = df[header_df[self.ui.spinBox_x.value() - 1]]  # .tolist()
                y = df[header_df[self.ui.spinBox_y.value() - 1]]  # .tolist()
                """
                Si le séparateur décimal est la virgule alors elle est remplacée par le 'point'.  
                """
                print("%%%%%%%%% :", header.split(data_delimiter), df.iloc[0, 0])
                if "," in str(df.iloc[0, 0]):
                    x = [float(str(i).replace(",", ".")) for i in x]
                    y = [float(str(i).replace(",", ".")) for i in y]

                """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                self.x_label = "{}".format(header_df[self.ui.spinBox_x.value() - 1])
                self.y_label = "{}".format(header_df[self.ui.spinBox_y.value() - 1])

                print(self.x_label, "\n", self.y_label)
                print("l'extension du fichier : ", pathlib.Path(self.filename).suffix)
                return x, y
            else:
                message_box.message_box_critical_index_error()
                return [], []
        else:
            message_box.message_box_critical_index_error()
            print(header)
            # self.x_label = "x"
            # self.y_label = "y"
            return [], []

    def get_data_x_y(self):
        if self.file_extension in [".txt", ".csv"]:
            return self._get_xy_txt_csv()
        else:
            return [], []

    def graph(self):
        """
        Returns: Le tracé de y en fonction de x.
        """

        self.ui.mycanvas.axes.clear()
        # self.ui.mycanvas.axes.cla()
        self.ui.mycanvas.add_arrows()

        x = self.model.x
        y = self.model.y

        self.ui.mycanvas.axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.plot_line_2d, = self.ui.mycanvas.axes.plot(x, y, color='r', lw=1.5, markersize=7, marker='+',
                                                        picker=30)
        self.ui.mycanvas.axes.set_xlabel(self.x_label, color='black', fontsize=10)
        self.ui.mycanvas.axes.set_ylabel(self.y_label, color='black', fontsize=10)
        #    self.ui.canvas.figure.tight_layout()

        self.onpick_event = mpl_canvas_onpick_event.OnpickEvent(self.ui.mycanvas.axes, x, y, self.ui.tableView)
        self.ui.mycanvas.figure.canvas.mpl_connect('pick_event', self.onpick_event.onpick)
        self.ui.mycanvas.figure.canvas.draw_idle()

    def insert_row(self):
        if len(self.ui.tableView.selectedIndexes()) == 0:
            self.model.insertRows(self.model.rowCount(), 1)
        else:
            rows = list(set([index.row() for index in self.ui.tableView.selectedIndexes()]))
            for row in rows:  # [::-1]:
                self.model.insertRows(row + 1, 1)
        try:
            self.graph()  # mise à jour du graphique
        except:
            pass

    def isometric_view(self):
        if self.filename:
            if self.ui.checkbox_isometric_view.isChecked():
                self.plot_line_2d.set_data(self.model.x, self.model.y)
                self.ui.mycanvas.axes.axis("equal")
                self.ui.mycanvas.figure.canvas.draw_idle()
            else:
                self.plot_line_2d.set_data(self.model.x, self.model.y)
                self.ui.mycanvas.axes.axis("tight")
                self.ui.mycanvas.toolbar.update()
                self.ui.mycanvas.figure.canvas.draw_idle()
                print("Isometric view is not checked")
        else:
            print("pas de graphique")

    def delete_row(self):
        selected_row = list(set([index.row() for index in self.ui.tableView.selectedIndexes()]))

        if len(selected_row) > 0:
            self.model.remove_rows(selected_row)
        self.graph()

    def sort_x_ascending(self):
        self.model.sort(0, order=Qt.AscendingOrder)
        self.graph()

    def sort_x_descending(self):
        self.model.sort(0, order=Qt.DescendingOrder)
        self.graph()

    def sort_y_ascending(self):
        self.model.sort(1, order=Qt.AscendingOrder)
        self.graph()

    def sort_y_descending(self):
        self.model.sort(1, order=Qt.DescendingOrder)
        self.graph()

    def move_row_down(self):
        rows = list(set([index.row() for index in self.ui.tableView.selectedIndexes()]))
        for row in rows:
            if row < self.model.rowCount() - 1:  # on s'arrête à la dernière ligne du tableau
                self.model.moveRowDown(row)
        self.graph()

    def move_row_up(self):
        rows = list(set([index.row() for index in self.ui.tableView.selectedIndexes()]))
        for row in rows:
            if 0 < row:  # on s'arrête lorsqu'on est à l'index 0 ie la première ligne
                self.model.moveRowUp(row)
        self.graph()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event == QtGui.QKeySequence.Copy:
                # self.copySelection()
                self.copy_table()
                print("copie")
                return True
            elif event == QtGui.QKeySequence.Paste:
                # self.pasteSelection()
                self.paste_table()
                return True
        elif event.type() == QEvent.ContextMenu:

            # a context menu for the copy/paste operations
            menu = QtWidgets.QMenu()
            copyAction = menu.addAction('Copy')
            # copyAction.triggered.connect(self.copySelection)
            # self.button_copy.triggered.connect(self.copyTable)
            pasteAction = menu.addAction('Paste')
            # pasteAction.triggered.connect(self.pasteSelection)
            #  self.button_paste.triggered.connect(self.pasteTable)
            if not self.ui.tableView.selectedIndexes():
                pass
                # no selection available, both copy and paste are disabled
                # copyAction.setEnabled(False)

            # if not self.clipboard:
            #     pass
            #     # no clipboard contents, paste is disabled
            #  pasteAction.setEnabled(False)
            #     self.button_paste.setEnabled(False)
            #     menu.exec(event.globalPos())
            # menu.exec(event.globalPos())
            return True
        # self.button_copy.setEnabled(False)
        # self.button_paste.setEnabled(False)
        return super(ApplicationWindow, self).eventFilter(source, event)

    def copySelection(self):
        # clear the current contents of the clipboard
        self.clipboard.clear()
        selected = self.tableView.selectedIndexes()
        rows = []
        columns = []
        # cycle all selected items to get the minimum row and column, so that the
        # reference will always be [0, 0]
        for index in selected:
            rows.append(index.row())
            columns.append(index.column())
        minRow = min(rows)
        minCol = min(columns)
        print(minCol)
        print(minRow, columns)
        for index in selected:
            # append the profile of each selected index
            self.clipboard.append((index.row() - minRow, index.column() - minCol, index._data()))
            # self.clipboard.append((index.row(), index.column() , index.profile()))

    def pasteSelection(self):
        if not self.clipboard:
            return
        current = self.tableView.currentIndex()
        if not current.isValid():
            # in the rare case that there is no current index, use the first row
            # and column as target
            current = self.model.index(0, 0)

        firstRow = current.row()
        firstColumn = current.column()

        # optional: get the selection model so that pasted indexes will be
        # automatically selected at the end
        selection = self.tableView.selectionModel()
        print(self.clipboard)
        for row, column, data in self.clipboard:
            # get the index, with rows and columns relative to the current
            # index = self.model.index(firstRow + row, firstColumn + column)
            index = self.model.index(firstRow, column)

            # set the profile for the index
            self.model.setData(index, data, Qt.EditRole)  # Qt.DisplayRole)
            # add the index to the selection
            selection.select(index, selection.Select)

        # apply the selection model
        self.tableView.setSelectionModel(selection)

    def copy_table(self):
        if len(self.ui.tableView.selectedIndexes()) == 0:
            self.model.copy_table(0, self.model.rowCount())
        else:
            rows = list(set([index.row() for index in self.ui.tableView.selectedIndexes()]))
            rows.sort()  # pour trier la liste afin de respecter l'ordre des lignes sélectionnées en collant
            print(rows)
            df = self.model._data.loc[rows, :]
            df.to_clipboard(header=None, index=False, excel=True, sep='\t')

    def paste_table(self):
        # self.tableView.clearSelection()
        if len(self.ui.tableView.selectedIndexes()) == 0:
            # pass
            self.model.paste_table(self.model.rowCount())
        else:
            rows = list(set([index.row() for index in self.ui.tableView.selectedIndexes()]))
            # rows.sort()  # pour trier la liste afin de respecter l'ordre des lignes sélectionnées en collant
            for row in rows:
                self.model.paste_table(row + 1)
                # try:
                #     self.model.pasteTable(row + 1)
                # except:
                #     print("Le collage n'est pas réussi")
            print(rows)
        self.graph()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())
