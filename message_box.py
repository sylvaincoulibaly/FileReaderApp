from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QComboBox, QApplication

_translate = QtCore.QCoreApplication.translate


def message_box_critical():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    # msg.setIcon(QMessageBox.Warning)
    msg.setText(_translate("MainWindow", "       Warning"))
    # msg.setInformativeText('Vérifiez que vous avez choisi un fichier .csv ')
    msg.setInformativeText(_translate("MainWindow", "Choose a CSV file"))
    msg.setWindowTitle(_translate("MainWindow", "Error "))
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)
    msg.exec_()


def message_box_critical_index_error():
    msg = QMessageBox()
    # msg.setIcon(QMessageBox.Critical)
    msg.setIcon(QMessageBox.Warning)
    # msg.setText("        Attention")
    # msg.setInformativeText('Vérifiez les colonnes sélectionnées et le séparateur de colonnes')
    msg.setInformativeText(_translate("MainWindow", 'Invalid column separator'))
    msg.setWindowTitle(_translate("MainWindow", " Warning"))
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)
    # self.btn_plot.setEnabled(False)
    msg.exec_()


def message_box_critical_file_not_found_error():
    msg = QMessageBox()
    # msg.setIcon(QMessageBox.Critical)
    msg.setIcon(QMessageBox.Warning)
    # msg.setText(" Attention")
    # msg.setInformativeText('Vérifiez les colonnes sélectionnées et le séparateur de colonnes')
    msg.setInformativeText(_translate("MainWindow", 'No file selected'))
    msg.setWindowTitle(_translate("MainWindow", "Warning"))
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)
    msg.exec_()


def message_box_critical_index_error_x_column(combobox, column_number):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    # msg.setIcon(QMessageBox.Warning)
    msg.setText(_translate("MainWindow", "         Warning"))
    # msg.setInformativeText(
    #     'La colonne x sélectionnée n\'existe pas avec le séparateur de colonnes \'{}\' choisi. \n Si vous '
    #     'avez choisi le bon séparateur alors sélectionnez une autre colonne x'.format(
    #         self.csv_separator_combo.currentText()))
    msg.setInformativeText(_translate("MainWindow", "The selected {}-column doesn\'t exist with the "
                                                    "chosen column separator.\n"
                                                    "If \"{}\" is the correct column separator "
                                                    "then select another {}-column".format(
        column_number,
        combobox.currentText(), column_number)))
    msg.setWindowTitle(_translate("MainWindow", "Error"))
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)
    msg.exec_()


def message_box_critical_index_error_y_column(combobox):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    # msg.setIcon(QMessageBox.Warning)
    msg.setText(_translate("MainWindow", "    Warning"))
    # msg.setInformativeText('La colonne y sélectionnée n\'existe pas avec ce séparateur de colonnes')
    # msg.setInformativeText(
    #     'La colonne y sélectionnée n\'existe pas avec le séparateur de colonnes \'{}\' choisi. \n Si vous '
    #     'avez choisi le bon séparateur alors sélectionnez une autre colonne y'.format(
    #         self.csv_separator_combo.currentText()))
    msg.setInformativeText(_translate("MainWindow", "The selected y-column doesn\'t exist with the "
                                                    "chosen column separator.\n") +
                           _translate("MainWindow", "If ") + f"{combobox.currentText()} " +
                           _translate("MainWindow", "is the correct column separator then select another y-column."))

    msg.setWindowTitle(_translate("MainWindow", "Error"))
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)
    msg.exec_()


def msgbtn(i):
    print("button pressed:", i.text())
