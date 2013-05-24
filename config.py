#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


from PyQt4.Qt import (Qt, QWidget, QGridLayout, QLabel, QLineEdit)


class ConfigWidget(QWidget):

    def __init__(self, plugin_action):
        QWidget.__init__(self)
        self.plugin_action = plugin_action

        from calibre_plugins.beam_ebooks_downloader.prefs import prefs

        print 'My Prefs are (%s)' % (prefs)
        print '    methods are (%s)' % (dir(prefs))

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.labelUrlBase = QLabel('URL:')
        self.layout.addWidget(self.labelUrlBase, 0, 0)

        self.urlbase = QLineEdit(self)
        if prefs.__getitem__(prefs.URLBASE) is not None:
            self.urlbase.setText(prefs.__getitem__(prefs.URLBASE))
        self.urlbase.setReadOnly(True)
        self.layout.addWidget(self.urlbase, 0, 1)
        self.labelUrlBase.setBuddy(self.urlbase)

        self.labelUserName = QLabel('Username:')
        self.layout.addWidget(self.labelUserName, 1, 0)

        self.username = QLineEdit(self)
        if prefs.__getitem__(prefs.USERNAME) is not None:
            self.username.setText(prefs.__getitem__(prefs.USERNAME))
        self.layout.addWidget(self.username, 1, 1)
        self.labelUserName.setBuddy(self.username)

        self.labelPassword = QLabel('Password')
        self.layout.addWidget(self.labelPassword, 2, 0)

        self.password = QLineEdit(self)
        if prefs.__getitem__(prefs.PASSWORD) is not None:
            self.password.setText(prefs.__getitem__(prefs.PASSWORD))
        self.layout.addWidget(self.password, 2, 1)
        self.labelPassword.setBuddy(self.password)


    def save_settings(self):
        from calibre_plugins.beam_ebooks_downloader.prefs import prefs

        # Copy any data necessary into the prefs object
        prefs.__setitem__(prefs.USERNAME, '%s' % self.username.text())
        prefs.__setitem__(prefs.PASSWORD, '%s' % self.password.text())
        # TODO proper hashing somewhere, maybe even in 'migrate'
        prefs.__setitem__(prefs.HASHED_PASSWORD, '%s' % self.password.text())

        # And save it...
        prefs.save()
