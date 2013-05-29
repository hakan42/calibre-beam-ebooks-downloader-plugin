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


from PyQt4.Qt import (Qt, QWidget, QGridLayout, QLabel, QLineEdit)


class ConfigWidget(QWidget):

    def __init__(self, plugin_action, prefs):
        QWidget.__init__(self)
        self.plugin_action = plugin_action
        self.prefs = prefs

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.labelUrlBase = QLabel('URL:')
        self.layout.addWidget(self.labelUrlBase, 0, 0)

        self.urlbase = QLineEdit(self)
        if prefs[prefs.URLBASE] is not None:
            self.urlbase.setText(prefs[prefs.URLBASE])
        self.urlbase.setReadOnly(True)
        self.layout.addWidget(self.urlbase, 0, 1)
        self.labelUrlBase.setBuddy(self.urlbase)

        self.labelUserName = QLabel('Username:')
        self.layout.addWidget(self.labelUserName, 1, 0)

        self.username = QLineEdit(self)
        if prefs[prefs.USERNAME] is not None:
            self.username.setText(prefs[prefs.USERNAME])
        self.layout.addWidget(self.username, 1, 1)
        self.labelUserName.setBuddy(self.username)

        self.labelPassword = QLabel('Password')
        self.layout.addWidget(self.labelPassword, 2, 0)

        self.password = QLineEdit(self)
        if prefs[prefs.PASSWORD] is not None:
            self.password.setText(prefs[prefs.PASSWORD])
        self.layout.addWidget(self.password, 2, 1)
        self.labelPassword.setBuddy(self.password)


    def save_settings(self):

        # Copy any data necessary into the prefs object
        self.prefs[self.prefs.USERNAME, '%s' % self.username.text()]
        self.prefs[self.prefs.PASSWORD, '%s' % self.password.text()]
        # TODO proper hashing somewhere, maybe even in 'migrate'
        self.prefs[self.prefs.HASHED_PASSWORD, '%s' % self.password.text()]

        # And save it...
        self.prefs.save()
