#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


from calibre.utils.config import JSONConfig

# Set defaults used by all.  Library specific settings continue to
# take from here.
default_prefs = {}
# default_prefs['personal.ini'] = get_resources('plugin-example.ini')

# This is where all preferences for this plugin will be stored
plugin_prefs = JSONConfig('plugins/Beam EBooks Downloader')


class PrefsFacade():

    def __init__(self,passed_db=None):
        self.default_prefs = default_prefs
        self.libraryid = None
        self.current_prefs = None
        self.passed_db=passed_db

# Return myself
prefs = PrefsFacade()
