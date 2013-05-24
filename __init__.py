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
    can_be_disabled = True

    version = (0, 5, 0)

    # Minium is 0.9.23 for the CLI support from this version on
    minimum_calibre_version = (0, 9, 23)


    def is_customizable(self):
        '''
        This method must return True to enable customization via
        Preferences->Plugins
        '''
        return True


    def config_widget(self):
        '''
        Implement this method and :meth:`save_settings` in your plugin to
        use a custom configuration dialog.

        This method, if implemented, must return a QWidget. The widget can have
        an optional method validate() that takes no arguments and is called
        immediately after the user clicks OK. Changes are applied if and only
        if the method returns True.
        '''
        if self.actual_plugin_:
            from calibre_plugins.beam_ebooks_downloader.config import ConfigWidget
            return ConfigWidget(self.actual_plugin_)


    def save_settings(self, config_widget):
        '''
        Save the settings specified by the user with config_widget.

        :param config_widget: The widget returned by :meth:`config_widget`.
        '''
        if config_widget is not None:
            config_widget.save_settings()

        # Apply the changes
        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()


    def cli_main(self, argv):
        from calibre.utils.config import prefs as calibre_prefs
        from calibre.library import db
        from optparse import OptionParser      

        from calibre_plugins.beam_ebooks_downloader.prefs import prefs

        print 'Here I Am'

        print 'My Prefs are (%s)' % (prefs)
        print '    methods are (%s)' % (dir(prefs))
        print '    library id is (%s)' % (prefs.libraryid)

        print 'Calibre Prefs are (%s)' % (calibre_prefs)
        print '    methods are (%s)' % (dir(calibre_prefs))

        pass
