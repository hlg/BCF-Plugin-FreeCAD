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
This file provides the view part of the comment list. This list has the
speciality of letting a button appear over the list item the mouse is currently
hovering over. Its model counter part is the CommentModel.
"""

import logging
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import bcfplugin
from bcfplugin.rdwr.viewpoint import Viewpoint

logger = bcfplugin.createLogger(__name__)


class CommentView(QListView):

    """ View showing comment to the user.

    The comment elements are drawn by the CommentDelegate. This class mainly
    maintains the delete button that appears over the "mouse hovered" comment.
    It also emits the event where a comment referencing a viewpoint is selected.
    At all times at most one delete button will be shown/drawn.
    """

    specialCommentSelected = Signal((Viewpoint))
    """ Emitted when a comment, referencing a viewpoint is selected. """


    def __init__(self, parent = None):

        QListView.__init__(self, parent)
        self.setMouseTracking(True)
        self.lastEnteredIndex = None
        """ Index of the list item over whose are the mouse hovered at last """
        self.entered.connect(self.mouseEntered)
        self.delBtn = None
        """ Reference to the delete button. """

        # create editor for a double left click on a comment
        self.doubleClicked.connect(lambda idx: self.edit(idx))


    @Slot()
    def mouseEntered(self, index):

        """ Display a delete button if the mouse hovers over a comment.

        The button is then wired to a dynamically created clicked handler. This
        handler will be passed the index of the hovered over element as
        parameter. """

        if self.delBtn is not None:
            self.deleteDelBtn()

        options = QStyleOptionViewItem()
        options.initFrom(self)

        btnText = self.tr("Delete")
        deleteButton = QPushButton(self)
        deleteButton.setText(btnText)
        deleteButton.clicked.connect(lambda: self.deleteElement(index))

        buttonFont = deleteButton.font()
        fontMetric = QFontMetrics(buttonFont)
        btnMinSize = fontMetric.boundingRect(btnText).size()
        deleteButton.setMinimumSize(btnMinSize)

        itemRect = self.rectForIndex(index)
        x = itemRect.width() - deleteButton.geometry().width()
        vOffset = self.verticalOffset() # scroll offset
        y = itemRect.y() - vOffset + itemRect.height() - deleteButton.geometry().height()
        deleteButton.move(x, y)

        deleteButton.show()
        self.delBtn = deleteButton


    def currentChanged(self, current, previous):

        """ If the current comment links to a viewpoint then select that
        viewpoint in viewpointsList.  """

        model = current.model()
        if model is None:
            # no topic is selected, so no comments are loaded
            return

        viewpoint = model.referencedViewpoint(current)
        if viewpoint is not None:
            self.specialCommentSelected.emit(viewpoint)


    def resizeEvent(self, event):

        """ Propagates the new width of the widget to the delegate """

        newSize = self.size()
        self.itemDelegate().setWidth(newSize.width())
        QListView.resizeEvent(self, event)


    @Slot()
    def deleteDelBtn(self):

        """ Delete the comment delete button from the view. """

        if self.delBtn is not None:
            self.delBtn.deleteLater()
            self.delBtn = None


    def deleteElement(self, index):

        """ Handler for deleting a comment when the comment delete button was
        pressed """

        success = index.model().removeRow(index)
        if success:
            self.deleteDelBtn()
        else:
            logger.error("Could not delete comment.")


