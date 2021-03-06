"""
Copyright (C) 2019 PODEST Patrick

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

"""
Author: Patrick Podest
Date: 2019-08-16
Github: @podestplatz

**** Description ****
This file provides the view part of the SnapshotList. This list displays
pictures in a horizontal fashion, thereby granting every picture an equal
amount of space, depending on the current width of the widget.
"""

import logging
from PySide2.QtWidgets import QListView, QLabel
from PySide2.QtCore import *
from PySide2.QtGui import *

import bcfplugin
import bcfplugin.util as util

logger = bcfplugin.createLogger(__name__)


class SnapshotView(QListView):

    """ Custom list, showing elements horizontally and setting their size to fit
    the window.

    Elements take up equal space in the list view. If there are N elements to be
    displayed, each one gets WIDTH/N units of the width of the view. In case of
    resizing the new sizes are calculated automatically.
    """

    def __init__(self, parent = None):

        QListView.__init__(self, parent)
        screen = util.getCurrentQScreen()
        ppm = screen.logicalDotsPerInch() / util.MMPI
        """ Pixels per millimeter """

        self.minIconSize = QSize(ppm * 20, ppm * 20)
        """ Minimum size of an icon is 2x2cm. """

        self.doubleClicked.connect(self.openSnapshot)
        self.setFlow(QListView.LeftToRight)


    def resizeEvent(self, event):

        """ Recalculate the size each element is allowed to occupy. """

        QListView.resizeEvent(self, event)

        newSize = self.size()
        rowCount = self.model().rowCount()
        rowCount = rowCount if rowCount > 0 else 1
        marginsLeftRight = (self.contentsMargins().left() +
                self.contentsMargins().right())
        marginsTopBottom = (self.contentsMargins().top() +
                self.contentsMargins().bottom())

        newItemWidth = newSize.width()
        newItemWidth -= self.spacing() * (rowCount)
        newItemWidth -= marginsLeftRight
        newItemWidth /= rowCount
        newItemSize = QSize(newItemWidth, newSize.height())

        # use minimum values if result is too small
        if (newItemWidth < self.minIconSize.width()):
            newItemSize.setWidth(self.minIconSize.width())
        if (newItemSize.height() < self.minIconSize.height()):
            newItemSize.setHeight(self.minIconSize.height())

        self.model().setSize(newItemSize)
        self.setIconSize(newItemSize)


    @Slot()
    def openSnapshot(self, idx):

        """ Opens the snapshot in original resolution an a new label opened in a
        separate window. """

        img = self.model().realImage(idx)
        lbl = QLabel(self)
        lbl.setWindowFlags(Qt.Window)
        lbl.setPixmap(img)
        lbl.show()
