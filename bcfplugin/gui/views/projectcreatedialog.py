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
Provides the project create dialog. This dialog is invoked when a new project
shall be created. Its only responsibility is to request the name of the
project in order for it to be able to be created.
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import bcfplugin
import bcfplugin.util as util
from bcfplugin.gui import views as view
import bcfplugin.gui.models as model
from bcfplugin.rdwr.topic import Topic

logger = bcfplugin.createLogger(__name__)


class ProjectCreateDialog(QDialog):

    def __init__(self, parent = None):

        QDialog.__init__(self, parent)
        self.setWindowTitle("Create new Project")

        mainLayout = QVBoxLayout(self)
        formLayout = QFormLayout()

        self.nameEdit = QLineEdit()
        self.nameEdit.setObjectName("Project Name")

        #extSchemaUriEdit = QLineEdit()
        #extSchemaUriEdit.setObjectName("Extension Schema Uri")

        submitBtn = QPushButton(self.tr("Submit"))
        submitBtn.clicked.connect(self.createProject)

        self.notificationLabel = view.createNotificationLabel()

        formLayout.addRow("Project Name", self.nameEdit)
        #formLayout.addRow("Extension Schema Uri", extSchemaUriEdit)

        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(submitBtn)
        mainLayout.addWidget(self.notificationLabel)


    def createProject(self):

        name = self.nameEdit.text()
        extSchema = "" #extSchemaUriEdit()
        if not model.createProject(name, extSchema):
            view.showNotification(self, "Project could not be created.")
        else:
            self.done(0)
