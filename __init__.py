#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'

# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import InterfaceActionBase

# Apparently the name for this class doesn't matter
class Downloader(InterfaceActionBase):

    name = 'Beam EBooks Downloader'
    actual_plugin = 'calibre_plugins.beam_ebooks_downloader.action:BeamEbooksDownloaderAction'
    description = _('UI plugin to download ebooks from Beam Ebooks.')
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Hakan Tandogan'

    version = (0, 5, 0)

    # Minium is 0.9.23 for the CLI support from this version on
    minimum_calibre_version = (0, 9, 23)


    def cli_main(self,argv):
        from optparse import OptionParser      

        print 'Here I Am'

        pass
