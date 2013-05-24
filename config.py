#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


from PyQt4.Qt import (Qt, QWidget, QHBoxLayout, QLabel, QLineEdit)


class ConfigWidget(QWidget):

    def __init__(self, plugin_action):
        QWidget.__init__(self)
        self.plugin_action = plugin_action

        self.l = QHBoxLayout()
        self.setLayout(self.l)

        self.label = QLabel('Hello world &message:')
        self.l.addWidget(self.label)

        self.msg = QLineEdit(self)
        # self.msg.setText(prefs['hello_world_msg'])
        self.msg.setText('Blurch Furbl')
        self.l.addWidget(self.msg)
        self.label.setBuddy(self.msg)

    def save_settings(self):
        from calibre_plugins.beam_ebooks_downloader.prefs import prefs

        # Copy any data necessary into the prefs object
        prefs.__setitem__(prefs.DUMMY, '%s' % self.msg.text())

        # And save it...
        prefs.save()
