# -----------------------------------------------------------------------------
# Name:        iodefs.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2019 Council for Geoscience
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
"""Import and export data."""

import os
from PyQt5 import QtWidgets
import segyio


class ImportSEGY():
    """
    Import Data.

    Attributes
    ----------
    name : str
        item name
    pbar : progressbar
        reference to a progress bar.
    parent : parent
        reference to the parent routine
    outdata : dictionary
        dictionary of output datasets
    ifile : str
        input file name. Used in main.py
    ext : str
        filename extension
    """

    def __init__(self, parent=None):
        self.ifile = ''
        self.name = 'Import Data: '
        self.ext = ''
        self.pbar = None
        self.parent = parent
        self.indata = {}
        self.outdata = {}

    def settings(self):
        """
        Entry point into item.

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        ext = 'SEGY (*.sgy)'

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent, 'Open SEGY File', '.', ext)
        if not filename:
            return False

        os.chdir(os.path.dirname(filename))
        self.ifile = filename

        dat = segyio.open(filename, ignore_geometry=True)

        if dat is None:
            QtWidgets.QMessageBox.warning(self.parent, 'Error',
                                          'Could not import dataset. ',
                                          QtWidgets.QMessageBox.Ok)
            return False

        output_type = 'ESEIS'

        self.outdata[output_type] = dat
        return True


class ExportSEGY():
    """
    Export Data.

    Attributes
    ----------
    name : str
        item name
    pbar : progressbar
        reference to a progress bar.
    parent : parent
        reference to the parent routine
    outdata : dictionary
        dictionary of output datasets
    ifile : str
        input file name. Used in main.py
    ext : str
        filename extension
    """

    def __init__(self, parent):
        self.ifile = ''
        self.name = 'Export Data: '
        self.ext = ''
        self.pbar = None
        self.parent = parent
        self.indata = {}
        self.outdata = {}

    def run(self):
        """
        Run.

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        self.parent.process_is_active(True)

        if 'ESEIS' in self.indata:
            data = self.indata['ESEIS']
        else:
            print('No SEGY data')
            self.parent.process_is_active(False)
            return False

        ext = 'SEGY (*.sgy)'

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, 'Save File', '.', ext)

        if filename == '':
            self.parent.process_is_active(False)
            return False

        os.chdir(os.path.dirname(filename))

        self.ifile = str(filename)

        print('Export Data Busy...')

        self.export_segy(data)

        print('Export SEGY Finished!')
        self.parent.process_is_active(False)
        return True

    def export_segy(self, dat):
        """
        Export to SEGY format.

        Parameters
        ----------
        dat : SEGY Data
            dataset to export

        Returns
        -------
        None.

        """
        src = self.indata['ESEIS']

        spec = segyio.tools.metadata(src)
        with segyio.create(self.ifile, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin
            dst.header = src.header
            dst.trace = src.trace
