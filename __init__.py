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

# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import InterfaceActionBase
from calibre.library import db

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
            from calibre_plugins.beam_ebooks_downloader.prefs import PrefsFacade

            my_db = db(path=None, read_only=True)
            prefs = PrefsFacade(my_db)
            return ConfigWidget(self.actual_plugin_, prefs)


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
        from optparse import OptionParser      

        from calibre_plugins.beam_ebooks_downloader.prefs import PrefsFacade

        my_db = db(path=None, read_only=False)

        # print 'Database is (%s)' % (prefs._get_db())
        print 'Database is (%s)' % (my_db)

        prefs = PrefsFacade(my_db)

        print 'My Prefs are (%s)' % (prefs)
        print '    methods are (%s)' % (dir(prefs))
        print '    library id is (%s)' % (prefs.get_library_uuid())

        print 'Calibre Prefs are (%s)' % (calibre_prefs)
        print '    methods are (%s)' % (dir(calibre_prefs))

        from calibre_plugins.beam_ebooks_downloader.downloader import BeamEbooksDownloader
        downloader = BeamEbooksDownloader(prefs, self.version)

        # Loop over all accounts until we have support for selection
        for account_id in prefs[prefs.ACCOUNTS]:
            account = prefs[prefs.ACCOUNTS][account_id]
            account[prefs.ACCOUNT_ID] = account_id
            print "Account: '%s'" % account

            if account[prefs.ENABLED]:
                downloader.login(account)

                if downloader.successful_login == False:
                    print "Failed to log in..."
                else:
                    print "Parsing document tree now..."
                    # Temporarily...
                    # downloader.recursive_descent(prefs[prefs.URLBASE] + "/aldiko/bibuebersicht.php5?user=" + downloader.beamid)
                    # downloader.recursive_descent(prefs[prefs.URLBASE] + "/aldiko/pakete.php5?user=" + downloader.beamid)
                    downloader.recursive_descent(prefs[prefs.URLBASE])
                    # downloader.recursive_descent(prefs[prefs.URLBASE] + "/kunden/abos.php5")
                    downloader.download_ebooks()

        pass
