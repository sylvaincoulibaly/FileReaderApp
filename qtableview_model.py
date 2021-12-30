import pandas as pd

from PyQt5.QtWidgets import QMessageBox, QStyledItemDelegate, QLineEdit
from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel, QVariant


class PandasModelEditable(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame, table_header=None):
        QAbstractTableModel.__init__(self)
        if table_header is None:
            self.header = ["x", "y"]
        else:
            self.header = table_header

        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                value = self._data.iloc[index.row()][index.column()]
                if isinstance(value, float):
                    # Render float to 4 dp
                    return "%.4f" % value  # les valeurs sont arrondies à 4 chiffres après la virgule

                return str(self._data.iloc[index.row(), index.column()])
                # return str(self._data[index.column()][index.row()])

            column_count = self.columnCount()
            for column in range(0, column_count):
                if index.column() == column and role == Qt.TextAlignmentRole:
                    return Qt.AlignHCenter | Qt.AlignVCenter

            # if role == Qt.BackgroundRole and index.column() == 1:  # role == Qt.BackgroundRole --> pour colorier la
            #     # colonne et role == Qt.ForegroundRole pour les valeurs
            #     # See below for the profile structure.
            #     return QtGui.QColor("#ededed")  # (Qt.lightGray)

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # Si nous sommes dans l'orientation Horizontal (header horizontal), avec le rôle DisplayRole, nous renvoyons
        # le texte correspondant à la section (colonne).
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # return self._data.columns[section]
            return self.header[section]
        """ Pour afficher les numéros de ligne : """
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[section] + 1
        return None

    def setData(self, index, value, role=Qt.EditRole):
        # row = index.row()
        # column = index.column()
        # if not value.isdigit():  # +++
        #     return False  # +++
        #
        # if not index.isValid():
        #     return None
        #
        # if role != Qt.EditRole:
        #     return False
        #
        # # row = index.row()
        # if row < 0 or row >= len(self.profile.values):
        #     return False
        #
        # # column = index.column()
        # if index.column() < 0 or index.column() >= self.profile.columns.size:
        #     return False

        # if not index.isValid():
        #     return False
        # if role != Qt.EditRole:
        #     return False
        # if index.row() < 0 or index.row() >= len(self.profile.values):

        if index.column() == 1:
            if isinstance(value, float):
                return None
        if not index.isValid():
            return False
        if role != Qt.EditRole:
            return False

        if index.row() < 0 or index.row() >= self.rowCount():
            return False
        if role == Qt.EditRole:
            try:
                self._data.iat[index.row(), index.column()] = float(value)
                self.dataChanged.emit(index,
                                      index)  # permet de mettre à jour le graphique lorsqu'on appuie sur ENTREE
                # via datavaluechanged()
                # print(self._data)
            except:  # l'exception permet au code de ne pas planter lorsqu'on n'a rien saisi dans une cellule et
                # qu'on clique sur une autre.
                # pass
                print('\n \n %%%%%%%%%%%% Valeur saisie invalide %%%%%%%%%%% \n \n ')
                self.QMessageBoxCritical(value)
            return True
        """le signal dataChanged() est envoyé à chaque fois que des éléments de données du modèle sont modifiés. Les
        changements des entêtes fournis par le modèle provoquent l'émission du signal headerDataChanged(). Si la
        structure des données sous-jacentes change, le modèle peut envoyer le signal layoutChanged() pour informer
        les vues qu'elles doivent réafficher les éléments présentés, en prenant la nouvelle structure en compte. """
        self.dataChanged.emit(index, index)
        self.layoutChanged.emit()
        # self.dataChanged.emit(index, index, (Qt.DisplayRole,))

        return False

    @staticmethod
    def QMessageBoxCritical(value):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        # msg.setIcon(QMessageBox.Warning)
        msg.setText("{} : Valeur saisie incorrecte ".format(value))
        # msg.setInformativeText('Vérifiez que vous avez choisi un fichier .csv ')
        msg.setInformativeText("Seules les valeurs numériques sont autorisées.")
        msg.setWindowTitle("Warning ")
        # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setStyleSheet("QLabel{min-width:150 px; font-size: 13px;} QPushButton{ width:20px; font-size: 12px};"
                          "background-color: Ligthgray ; color : gray;font-size: 8pt; color: #888a80;")
        msg.exec_()

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, QModelIndex())

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        # if index.column() == 0:
        #     return Qt.ItemIsSelectable | Qt.ItemIsEnabled  # la colonne des abscisses n'est pas éditable
        # else:
        #     return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    # @QtCore.pyqtSlot()
    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        indexes = [str(self.rowCount() + i) for i in range(count)]
        #    print(indexes)
        left = self._data[0:row]
        mid = pd.DataFrame(index=indexes, columns=self._data.columns)
        # mid.iloc[row][3].replace(np.nan, '', inplace=True)
        right = self._data[row + count - 1:self.rowCount()]
        self._data = pd.concat([left, mid, right])
        # for i in [3]:
        #     self._data.iloc[:, i].replace(np.nan, '', inplace=True)  # remplacer 'nan' par une chaine vide dans les
        #     # cols 3
        self._data.reset_index(drop=True, inplace=True)

        self.endInsertRows()
        # print(self.profile.dtypes)
        # print(mid.dtypes)
        self.layoutChanged.emit()

    # @QtCore.pyqtSlot()
    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count + 1)
        self._data.drop(self._data.index[row], inplace=True)

        self.endRemoveRows()
        self.layoutChanged.emit()
        print(self._data)

    def remove_rows1(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)

        left = self._data.iloc[0:row]
        #   print(left)
        right = self._data.iloc[row + count:self.rowCount()]
        self._data = pd.concat([left, right], axis=0, ignore_index=True)
        self.endRemoveRows()
        self.layoutChanged.emit()
        print(self._data)

    def remove_rows(self, list_row_selected, parent=QModelIndex()):
        # self.layoutAboutToBeChanged.emit()
        self.beginRemoveRows(parent, list_row_selected[0], list_row_selected[-1])
        self._data.drop(self._data.index[list_row_selected], inplace=True)
        self._data.reset_index(drop=True, inplace=True)  # il faut remettre le compteur des index à zéro pour
        # éviter le "plantage" du programme lors de l'appel de certaines fonctionnalités, telle que le
        # copier/coller
        self.endRemoveRows()

        self.layoutChanged.emit()

    def sort(self, column, order=Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        colname = self._data.columns.tolist()[column]
        self._data.sort_values(colname, ascending=order == Qt.AscendingOrder, inplace=True)
        self._data.reset_index(inplace=True, drop=True)
        print(self._data)
        self.layoutChanged.emit()

    def moveRowDown(self, row_to_move, parent=QModelIndex()):
        target = row_to_move + 2
        self.beginMoveRows(parent, row_to_move, row_to_move, parent, target)
        block_before_row = self._data.iloc[0:row_to_move]
        # print(block_before_row)
        selected_row = self._data.iloc[row_to_move:row_to_move + 1]
        #    print(selected_row)
        after_selcted_row = self._data.iloc[row_to_move + 1:row_to_move + 2]
        #   print(after_selcted_row )
        block_after_row = self._data.iloc[row_to_move + 2:self.rowCount()]
        # print(block_after_row)
        self._data = pd.concat([block_before_row, after_selcted_row, selected_row, block_after_row], axis=0)
        self._data.reset_index(inplace=True, drop=True)
        self.endMoveRows()
        self.layoutChanged.emit()

    def moveRowUp(self, row_to_move, parent=QModelIndex()):
        target = row_to_move + 1
        self.beginMoveRows(parent, row_to_move - 1, row_to_move - 1, parent, target)
        block_before_row = self._data.iloc[0:row_to_move - 1]
        #   print(block_before_row)
        before_selected_row = self._data.iloc[row_to_move - 1:row_to_move]
        #  print(before_selected_row)
        selected_row = self._data.iloc[row_to_move:row_to_move + 1]
        #     print(selected_row)
        block_after_row = self._data.iloc[row_to_move + 1:self.rowCount()]
        # print(rblock_after_row)
        self._data = pd.concat([block_before_row, selected_row, before_selected_row, block_after_row], axis=0)
        self._data.reset_index(inplace=True, drop=True)
        self.endMoveRows()
        self.layoutChanged.emit()

    def copy_table(self, start_selection, end_selection):
        end_selection = self.rowCount()

        self._data.loc[start_selection:end_selection].to_clipboard(header=None, index=False, excel=True, sep='\t')

    def insert_df_to_idx(self, idx, df, df_insert):
        """
        Args:
            idx: is the index position in df where you want to insert new dataframe (df_insert)
            df: dataframe
            df_insert: dataframe to insert
        Returns: le dataframe df with df_insert inserted at index idx.
        """
        return df.iloc[:idx, ].append(df_insert).append(df.iloc[idx:, ]).reset_index(drop=True)

    def paste_table(self, insertion_index):
        self.layoutAboutToBeChanged.emit()
        df = pd.read_clipboard(header=None, skip_blank_lines=True, sep="\t",
                               names=self.header)
        self._data = self.insert_df_to_idx(insertion_index, self._data, df)
        print(self._data)
        self.layoutChanged.emit()

    @property
    def x(self):
        return self._data.iloc[:, 0].tolist()

    @property
    def y(self):
        return self._data.iloc[:, 1].tolist()

    @property
    def z(self):
        return self._data.iloc[:, 2].tolist()

    @property
    def name(self):
        return self._data.iloc[:, 3].tolist()

    def get_data(self):
        return self._data

    @property
    def station(self):
        return self._data.iloc[:, 4].tolist()

    def remove_duplicates_names(self):
        counter_list = []
        list_deleted_names = []
        # is_removed = False
        ind_ind = []
        for ind, name_point in enumerate(self.name):
            if name_point not in counter_list:
                counter_list.append(name_point)

            elif len(name_point.strip()) > 0 and name_point in counter_list:
                # is_removed = True
                ind_ind.append(ind)
                # self._data.iat[ind, 3] = ""
                if name_point not in list_deleted_names:
                    list_deleted_names.append(name_point)

        for ind in ind_ind:
            self._data.iat[ind, 3] = ""

    def data_contains_nan(self) -> bool:
        """
        Returns: Returns True if the QTableView() contains np.nan
        """
        return self._data.isnull().values.any()

    def delete_empty_rows(self):
        # for row in range(self.rowCount()):
        # print(self._data)
        # print(self._data.isnull().values.any())
        self.layoutAboutToBeChanged.emit()

        self._data.dropna(inplace=True)
        self._data.reset_index(drop=True,
                               inplace=True)  # il faut remettre le compteur des index à zéro pour

        # éviter le "plantage" du programme lors de l'appel de certaines fonctionnalités, telle que le
        # copier/coller
        self.layoutChanged.emit()
        print(self._data)


class Delegate(QStyledItemDelegate):
    # Lorsque l'on souhaite uniquement personnaliser l'édition des éléments dans une vue et non le rendu,
    # on doit redéfinir quatre méthodes
    def __init__(self, parent=None, setModelDataEvent=None):
        super(Delegate, self).__init__(parent)
        self.setModelDataEvent = setModelDataEvent

    def createEditor(self, parent, option, index):
        """
        Args:
            parent:
            option:
            index:
        Returns: Le widget (éditeur) pour éditer l'item se trouvant à l'index index.
        """
        index.model().data(index, Qt.DisplayRole)
        return QLineEdit(parent)

    def setEditorData(self, editor, index):
        """
        Args:
            editor: l'éditeur
            index: l'index
        Returns: permet de transmettre à l'éditeur editor les données à afficher à partir du modèle se trouvant
                à l'index index.
        """
        value = index.model().data(index, Qt.DisplayRole)  # DisplayRole
        editor.setText(str(value))  # récupère la valeur de la cellule et applique la méthode définie dans setData
        print('Donnée éditée dans la case [{},{}] :'.format(index.row(), index.column()), value)

    def setModelData(self, editor, model, index):
        """
        Args:
            editor: l'éditeur
            model: le modèle
            index: l'index
        Returns: permet de récupérer les données de l'éditeur et de les stocker à l'intérieur du modèle, à l'index
                identifié par le paramètre index
        """
        model.setData(index, editor.text())
        # if self.setModelDataEvent is not None:
        if not self.setModelDataEvent is None:
            self.setModelDataEvent()
        row = index.row()
        col = index.column()
        # récup de la valeur modifiée
        valeur = index.model().data(index, Qt.DisplayRole)
        print("Case: [{},{}]   Nouvelle valeur: {} \n".format(row, col, valeur))

    def updateEditorGeometry(self, editor, option, index):
        """
        Args:
            editor: l'éditeur
            option:
            index: l'index
        Returns: Permet de redimensionner l'éditeur à la bonne taille lorsque la taille de la vue change
        """
        editor.setGeometry(option.rect)
