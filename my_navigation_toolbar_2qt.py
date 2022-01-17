from PyQt5 import QtCore, QtGui

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

_translate = QtCore.QCoreApplication.translate


class MyNavigationToolbar2QT(NavigationToolbar2QT):
    def __init__(self, canvas, parent):
        self.my_canvas = canvas

        self.toolitems = [
            ('Home', "Reset original view", 'home', 'home'),
            # ('Home', 'Vue globale automatique', 'home', 'home'),
            (None, None, None, None),
            ('Back', "Back to previous view", 'back', 'back'),
            # ('Back', 'Retour à la vue précédente', 'back', 'back'),
            ('Forward', "Forward to next view", 'forward', 'forward'),
            # ('Forward', 'Passer à la vue suivante', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', "Pan axes with left mouse, zoom with right", 'move', 'pan'),
            # ('Pan', 'Panoramique des axes avec la souris gauche, zoom avec la droite', 'move', 'pan'),
            (None, None, None, None),
            ('Zoom', "Zoom rectangle", 'zoom_to_rect', 'zoom'),
            # ('Zoom', 'Zoom', 'zoom_to_rect', 'zoom'),
            #  ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            # ('Customize', 'Edit axis, curve and image parameters', 'qt4_editor_options', 'edit_parameters'),
            (None, None, None, None),
            ('Save', "Save the figure", 'filesave', 'save_figure'),
            # ('Save', 'Enregistrer la figure', 'filesave', 'save_figure'),
            (None, None, None, None),
            ('Cursor', 'Cursor', 'set_cursor', 'cursor'),

            # (None, None, None, None),
        ]

        NavigationToolbar2QT.__init__(self, canvas, parent)

        icon_btn_isometric_view = QtGui.QIcon()
        icon_btn_isometric_view.addPixmap(
            QtGui.QPixmap("resources/gtk-zoom-100.png"))
        # self.addSeparator()

        self._actions["cursor"].setIcon(icon_btn_isometric_view)
        self._actions["cursor"].setVisible(False)
        self.addSeparator()

        self.action_isometric_view = self.addAction(icon_btn_isometric_view,
                                                    "", self.isometric_view)
        self.action_isometric_view.setShortcut("Shift+W")

        self.addSeparator()

        icon_btn_non_isometric_view = QtGui.QIcon()
        icon_btn_non_isometric_view.addPixmap(
            QtGui.QPixmap("resources/gtk-zoom-fit.png"))
        self.action_auto_global_view = self.addAction(icon_btn_non_isometric_view,
                                                      "",
                                                      self.non_isometric_view)
        self.action_auto_global_view.setShortcut("Shift+X")
        self.addSeparator()
        # self.action_isometric_view.setCheckable(True)
        # self.action_auto_global_view.setCheckable(True)
        # a = self.addAction(icon_btn_isometric_view,
        #                    "test", self.func)
        # self._actions[self.func()] = a

    def isometric_view(self):
        self.my_canvas.axes.axis("equal")
        self.my_canvas.figure.canvas.draw_idle()
        # self.action_isometric_view.setCheckable(True)
        print("\nIsometric view enabled !!!")

    def non_isometric_view(self):
        self.my_canvas.axes.axis("tight")
        self.my_canvas.toolbar.update()
        self.my_canvas.figure.canvas.draw_idle()
        # self.action_auto_global_view.setCheckable(True)
        print("\nIsometric view disabled !!!")

    def toolitems_translation(self):
        self._actions['home'].setToolTip(_translate("MainWindow", "Reset original view"))
        self._actions['back'].setToolTip(_translate("MainWindow", "Back to previous view"))
        self._actions['forward'].setToolTip(_translate("MainWindow", "Forward to next view"))
        self._actions['pan'].setToolTip(_translate("MainWindow", "Pan axes with left mouse, zoom with right"))
        self._actions['zoom'].setToolTip(_translate("MainWindow", "Zoom rectangle"))
        self._actions['save_figure'].setToolTip(_translate("MainWindow", "Save the figure"))
        self.action_isometric_view.setToolTip(_translate("MainWindow", "Isometric view (Shift+W)"))
        self.action_auto_global_view.setToolTip(_translate("MainWindow", "Automatic global view (Shift+X)"))
