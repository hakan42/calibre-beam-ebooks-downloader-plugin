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

        accounts = self.prefs[self.prefs.ACCOUNTS]
        # Copy any data necessary into the prefs object

        # The primary account, as configured in the GUI above
        account = accounts.get('0', {})

        self.labelUrlBase = QLabel(_('URL'))
        self.layout.addWidget(self.labelUrlBase, 0, 0)

        self.urlbase = QLabel()
        if prefs[prefs.URLBASE] is not None:
            self.urlbase.setText(prefs[prefs.URLBASE])
        self.layout.addWidget(self.urlbase, 0, 1)
        self.labelUrlBase.setBuddy(self.urlbase)

        self.labelUserName = QLabel(_('Username'))
        self.layout.addWidget(self.labelUserName, 1, 0)

        self.username = QLineEdit(self)
        if account[prefs.USERNAME] is not None:
            self.username.setText(account[prefs.USERNAME])
        self.layout.addWidget(self.username, 1, 1)
        self.labelUserName.setBuddy(self.username)

        self.labelPassword = QLabel(_('Password'))
        self.layout.addWidget(self.labelPassword, 2, 0)

        self.password = QLineEdit(self)
        if account[prefs.PASSWORD] is not None:
            self.password.setText(account[prefs.PASSWORD])
        self.layout.addWidget(self.password, 2, 1)
        self.labelPassword.setBuddy(self.password)


    def save_settings(self):

        # TODO proper obfuscating somewhere, maybe even in 'migrate'

        accounts = self.prefs[self.prefs.ACCOUNTS]
        # Copy any data necessary into the prefs object

        # The primary account, as configured in the GUI above
        account_id = '0'
        account = accounts.get(account_id, {})
        account[self.prefs.ACCOUNT_ID] = account_id
        account[self.prefs.USERNAME] = '%s' % self.username.text()
        account[self.prefs.PASSWORD] = '%s' % self.password.text()
        account[self.prefs.OBFUSCATED_PASSWORD] = '%s' % self.password.text() 
        account[self.prefs.ENABLED] = True
        accounts[account_id] = account

        # Now the secondary account :-)
        account_id = '1'
        account = accounts.get(account_id, {})
        account[self.prefs.ACCOUNT_ID] = account_id
        if account.get(self.prefs.USERNAME) is None:
            account[self.prefs.USERNAME] = ''
            account[self.prefs.PASSWORD] = ''
            account[self.prefs.OBFUSCATED_PASSWORD] = ''
            account[self.prefs.ENABLED] = False
        accounts[account_id] = account

        # Now, put the hash back to the main prefs
        self.prefs[self.prefs.ACCOUNTS] = accounts

        # And save it...
        self.prefs.save()
