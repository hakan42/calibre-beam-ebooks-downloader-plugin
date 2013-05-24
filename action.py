#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'

# The class that all Interface Action plugin wrappers must inherit from
from calibre.gui2.actions import InterfaceAction

class BeamEbooksDownloaderAction(InterfaceAction):

    def apply_settings(self):
        from calibre_plugins.beam_ebooks_downloader.prefs import prefs

        # No need to do anything with prefs here, but we could.
        prefs
