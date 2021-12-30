from time import time

import numpy as np
from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtWidgets import QApplication


class OnpickEvent(object):
    def __init__(self, ax, x, y, tableview=None):
        """
        Args:
            ax: objet Axes.
            x: abscisse x1 du graphe (f(x1) = y1) à tracer.
            y: ordonnée y1 du graphe (f(x1) = y1) à tracer.
            tableview: tableau (de type QTableView) 'associé' au grahique.
        """
        self.ax = ax
        self.x = x
        self.y = y

        self.tableView = tableview
        self.counter_onclick = 0
        self.count = 0
        self.plot_selec()

        self.list_selected_points = []
        self.tableView.selectionModel().selectionChanged.connect(self.update_select_point_point)

    def select_row_pt_clicked(self, ind: int = 0):
        """
        Args:
             ind: Indice de la ligne où se trouve le point le plus proche 'visé'.
        Returns: Sélectionne la ligne (du tableau) correspondant au point le plus proche 'visé' à la suite de l'événement onpick.
        """
        if self.tableView is not None:
            selection_model = self.tableView.selectionModel()
            index = self.tableView.model().index(ind, 0)
            selection_model.select(index,
                                   QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect |
                                   QItemSelectionModel.Select)
            # In general for all the classes that inherit from QAbstractItemView(like QTableView, QTableWidget,
            # QListView, etc) there is the scrollTo method that is used internally to scrollToItem
            self.tableView.scrollTo(index)

    def select_qtableview_row(self, event):
        if self.tableView is not None:
            self.tableView.setFocus()
            ind = self.indice_points_onpick(event)
            dataidx_ecran = self.index_pt_plus_proche_ecran(event)
            self.select_row_pt_clicked(ind[dataidx_ecran])

    def update_select_point_point(self):
        if self.tableView is not None:
            rows = list(set([index.row() for index in self.tableView.selectedIndexes()]))
            if len(rows) > 1:
                for row in rows:
                    point = self.ax.plot(self.x[row], self.y[row], '+', c='Blue', markersize=8)
                    self.list_selected_points.append(point)
                    self.update_select_point_point_bis(self.x[row], self.y[row])

            elif len(rows) == 1:
                for row in rows:  #
                    # self.select_plot.set_data(self.x[row], self.y[row]
                    # self.ax.plot(self.x[row], self.y[row],'+', c='Blue', markersize=7)
                    # print(self.pt)
                    # if len(self.pt) > 0:
                    try:
                        [pl[0].set_data([], []) for pl in self.list_selected_points if
                         len(self.list_selected_points) > 1]
                    #  [pl[0].remove() for pl in self.pt[0:-2]]

                    except:
                        print("Probleme  de mise à jour ... update_select_point_point()")
                    try:
                        self.update_select_point_point_bis(self.x[row], self.y[row])
                    except:
                        print("index introuvable pour la mise à jour de l'affichage de la sélection du point."
                              "Editer les cases en 'nan'.")

            self.ax.figure.canvas.draw_idle()

    def plot_selec(self):
        try:
            self.selected_point, = self.ax.plot(self.x[0], self.y[0], '+', c='blue', markersize=8)
            self.selected_point.set_visible(False)
        except:
            print("tableau vide pour l'instant")

    # self.ax.figure.canvas.draw_idle()

    def update_select_point_point_bis(self, x_ind, y_ind):
        # if self.tableView is not None:
        #     rows = list(set([index.row() for index in self.tableView.selectedIndexes()]))
        #     for row in rows:  #
        self.selected_point.set_data(x_ind, y_ind)  # ,'+', c='Blue', markersize=7)
        self.selected_point.set_visible(True)
        self.ax.figure.canvas.draw_idle()  # nécessaire pour la mise à jour de l'affichage

    def plot_selection_point(self, x, y):
        """
        Args:
            x: abscisse
            y: ordonnée
        Returns: sélectionne le point du graphique correspond à la ligne sélectionnée dans le tableau.
        """
        if self.tableView is not None:
            self.select_point, = self.ax.plot(x, y, '+', c='Blue', markersize=7)
        else:
            self.select_point, = self.ax.plot([], [])

    @property
    def delta_x(self):
        """"
        Returns: la longueur entre les limites de la vue sur l'axe des x, c'est-à-dire |x_max_visible - x_min_visible|.
        """
        xgauche, xdroite = self.ax.get_xlim()
        delta_x = abs(xdroite - xgauche)
        return delta_x

    @property
    def delta_y(self):
        """
        Returns: la longueur entre les limites de la vue sur l'axe des y, c'est à dire |y_max_visible - y_min_visible|.
        """
        ybas, yhaut = self.ax.get_ylim()
        delta_y = abs(yhaut - ybas)
        return delta_y

    @staticmethod
    def indice_points_onpick(event):
        """
        Args: event
        Returns: le(s) indexe(s) du/des point(s) (plus précisement les coordonnées de points) capturé(s)
                 par l'événement onpick (voir picker)
        """
        return event.ind

    def points_onpick(self, event):
        """
        Args:
            event:
        Returns: une array contenant les coordonées des points qui se trouvent dans la zone définie par l'événement
        onpick (voir picker)

        """
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        points_onpick = np.array([(xdata[i], ydata[i]) for i in self.indice_points_onpick(event)])
        return points_onpick

    def distance_normee(self, event):
        """
        Args:
            event:
        Returns: la liste des distances normées (en m) entre les points situés dans la région définie par l'événement
         onpick (voir picker).
        """
        ind = event.ind
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        points_onpick = np.array([(xdata[i], ydata[i]) for i in ind])
        distances_normees = [(((x - event.mouseevent.xdata) / self.delta_x) ** 2 +
                              ((y - event.mouseevent.ydata) / self.delta_y) ** 2) ** (1 / 2) for (x, y) in
                             points_onpick]
        return distances_normees

    def position_souris(self, event):
        """
        Args:
            event:
        Returns: la position de la souris
        """
        pos_souris = [(event.mouseevent.xdata, event.mouseevent.ydata)]
        return pos_souris

    def distance_ecran(self, event):
        """
        Args:
            event:
        Returns: la liste des distances 'visuelles' entre les points situés dans la région définie par l'événement
        onpick (voir picker).
        """
        # self.ax.get_window_extent() retourne la boîte de délimitation des axes dans l'espace d'affichage ; args et
        # kwargs sont vides.
        # bbox : bounding box
        bbox = self.ax.get_window_extent().transformed(self.ax.figure.dpi_scale_trans.inverted())

        # bbox = self.ax.get_window_extent().transformed(self.ax.figure.dpi_scale_trans.inverted())
        ratio_w_sur_h = bbox.width / bbox.height  # le graphique est "ratio_w_sur_h fois plus large que haut"
        distances_ecran = [(((x - event.mouseevent.xdata) / (self.delta_x * ratio_w_sur_h)) ** 2 +
                            ((y - event.mouseevent.ydata) / self.delta_y) ** 2) ** (1 / 2) for (x, y) in
                           self.points_onpick(event)]
        return distances_ecran

    def distances(self, event):
        """
        Args: event:
        Returns: la liste des distances entre la position de la souris et tous les points se trouvant dans
        la zone définie par l'événement onpick ( voir picker)
        """
        distances = np.linalg.norm(self.points_onpick(event) - self.position_souris(event), axis=1)
        return distances

    def index_pt_plus_proche_ecran(self, event):
        """
         Args:
             event:
         Returns: indice du point le plus proche visuellement de la position du click.
         """
        dataidx_ecran = np.argmin(self.distance_ecran(event))
        return dataidx_ecran

    def point_plus_proche_ecran(self, event):
        point_onpick = self.points_onpick(event)
        datapos_ecran = point_onpick[self.index_pt_plus_proche_ecran(event)]
        return self.points_onpick(event)[self.index_pt_plus_proche_ecran(event)]  # datapos_ecran

    def index_pt_plus_proche(self, event):
        """
        Args:
            event:
        Returns: indice du point le plus proche de la position du click.
        """
        dataidx = np.argmin(self.distances(event))
        return dataidx

    def point_plus_proche(self, event):
        """
        Args:
            event:
        Returns: point le plus proche de la position du click
        """
        point_onpick = self.points_onpick(event)
        datapos = point_onpick[self.index_pt_plus_proche(event)]
        return datapos

    def annotate_onpick(self, x, y):
        """
        Args:
            x: abscisse du point à annoter.
            y: ordonnée du point à annoter.
        Returns: annote le point xy avec du texte text = xytext.
        """
        annotate_onpick = self.ax.annotate("X", xytext=(x, y),
                                           xy=(x, y), fontsize=9,
                                           bbox=dict(boxstyle='round,pad=0.8', fc='yellow', alpha=0.75),
                                           arrowprops=dict(arrowstyle='->',
                                                           connectionstyle='arc3,rad=0.',
                                                           color='blue'))
        return annotate_onpick

    def on_ylims_change(self, event_ax):
        print("updated ylims: ", event_ax.get_ylim())
        return event_ax.get_ylim()

    def onpick(self, event):
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier:
            start = time()
            print("******************************************")
            print("Onpick, nb points :", len(self.x))
            if event.mouseevent.inaxes == self.ax:
                # if event.mouseevent.xdata :# is not None and event.mouseevent.ydata is not None:
                self.select_qtableview_row(event)
                # self.update_select_point_point_bis(event.mouseevent.xdata, event.mouseevent.ydata)
                x_proche, y_proche = self.point_plus_proche_ecran(event)
                self.update_select_point_point_bis(x_proche, y_proche)
                # self.ax.figure.canvas.draw_idle()

            end = time()
            duree = end - start
            print("temps écoulé : ", duree)
            self.ax.figure.canvas.draw_idle()
