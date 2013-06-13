#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

#
# Copyright 2013 Hakan Tandogan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


from PyQt4.Qt import (Qt, QDialog, QWidget, QGridLayout, QVBoxLayout, QPushButton,
                      QLabel, QLineEdit, QMessageBox, QTextEdit)


class DownloadDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI
        self.db = gui.current_db

        # The GUI, created and layouted by hand...
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setWindowTitle('Beam EBooks Downloader')
        self.setWindowIcon(icon)

        self.log_area = QTextEdit('Log output', self)
        self.log_area.setReadOnly(True)
        self.log_area.setLineWrapMode(QTextEdit.NoWrap);
        self.log_area.setText("Blah")
        self.layout.addWidget(self.log_area)

        self.download_button = QPushButton('Download books', self)
        self.download_button.clicked.connect(self.download)
        self.layout.addWidget(self.download_button)

        self.conf_button = QPushButton('Configure this plugin', self)
        self.conf_button.clicked.connect(self.config)
        self.layout.addWidget(self.conf_button)

        self.resize(self.sizeHint())


    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        # Not necessary, the downloader will obtain fresh config anyway...
        # self.label.setText(prefs['hello_world_msg'])


    def download(self):
        print "Download button clicked (%s)" % (self)

        # insertPlainText inserts at the beginning of the log area...
        self.log_area.append("Another Click...")
        sb = self.log_area.verticalScrollBar()
        sb.setValue(sb.maximum())
