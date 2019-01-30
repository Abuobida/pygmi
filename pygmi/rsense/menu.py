# -----------------------------------------------------------------------------
# Name:        menu.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2018 Council for Geoscience
# Licence:     GPL-3.0
#
# This file is part of PyGMI
#
# PyGMI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGMI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
""" Clustering Menu Routines """

from PyQt5 import QtWidgets
from pygmi.bholes import iodefs
from pygmi.bholes import graphs


class MenuWidget():
    """
    Widget class to call the main interface

    This widget class creates the clustering menus to be found on the main
    interface. Normal as well as context menus are defined here.

    Attributes
    ----------
    parent : MainWidget
        Reference to MainWidget class found in main.py
    """
    def __init__(self, parent):

        self.parent = parent
        self.parent.add_to_context('Remote Sensing')
#        context_menu = self.parent.context_menu

# Normal menus
        self.menu = QtWidgets.QMenu(parent.menubar)
        self.menu.setTitle('Remote Sensing')
        parent.menubar.addAction(self.menu.menuAction())
        self.menu2 = self.menu.addMenu('Change Detection')

        self.action_create_list = QtWidgets.QAction(parent)
        self.action_create_list.setText("Create Scene List")
        self.menu2.addAction(self.action_create_list)
        self.action_create_list.triggered.connect(self.import_data)

        self.action_load_list = QtWidgets.QAction(parent)
        self.action_load_list.setText("Load Scene List")
        self.menu2.addAction(self.action_load_list)
        self.action_load_list.triggered.connect(self.import_data)

        self.menu.addSeparator()

        self.action_data_viewer = QtWidgets.QAction(parent)
        self.action_data_viewer.setText("View Change Data")
        self.menu2.addAction(self.action_data_viewer)
        self.action_data_viewer.triggered.connect(self.import_data)




# Context menus
#        context_menu['Remote Sensing'].addSeparator()
#
#        self.action_show_log = QtWidgets.QAction(self.parent)
#        self.action_show_log.setText("Show Borehole Log")
#        context_menu['Remote Sensing'].addAction(self.action_show_log)
#        self.action_show_log.triggered.connect(self.show_log)
#
#        self.action_export_data = QtWidgets.QAction(self.parent)
#        self.action_export_data.setText("Export Data")
#        context_menu['Cluster'].addAction(self.action_export_data)
#        self.action_export_data.triggered.connect(self.export_data)

#    def cluster_stats(self):
#        """ Basic Statistics """
#        self.parent.launch_context_item(show_table.ClusterStats)

    def import_data(self):
        """ Imports data"""
        fnc = iodefs.ImportData(self.parent)
        self.parent.item_insert("Io", "Import Data", fnc)

#    def export_data(self):
#        """ Export raster data """
#        self.parent.launch_context_item(iodefs.ExportData)

    def show_log(self):
        """ Show log data """
        self.parent.launch_context_item(graphs.PlotLog)