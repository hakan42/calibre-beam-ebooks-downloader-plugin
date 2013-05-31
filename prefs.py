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


from calibre.utils.config import JSONConfig
from calibre.gui2.ui import get_gui

SCHEMA_VERSION = 'SchemaVersion'
DEFAULT_SCHEMA_VERSION = 1.0

# This is where all preferences for this plugin will be stored
plugin_prefs = JSONConfig('plugins/Beam EBooks Downloader')


class PrefsFacade():

    URLBASE = 'Urlbase'

    ACCOUNTS = 'Accounts'

    USERNAME = 'Username'

    PASSWORD = 'Password'

    OBFUSCATED_PASSWORD = 'ObfuscatedPassword'

    ENABLED = 'Enabled'

    DOWNLOADS_PER_SESSION = 'DownloadsPerSession'

    def __init__(self, passed_db=None):
        self.libraryid = None
        self.plugin_prefs = plugin_prefs
        self.passed_db = passed_db

        # Set defaults
        self._init_defaults()
        # Ensure our config gets migrated
        self._migrate_config_if_required()

        url_base = self[self.URLBASE]
        if url_base is None:
            self[self.URLBASE] = self.default_prefs[self.URLBASE]
            self.save()

        accounts = self[self.ACCOUNTS]
        if accounts is None:
            self[self.ACCOUNTS] = self.default_prefs[self.ACCOUNTS]
            self.save()

        url_base = self[self.DOWNLOADS_PER_SESSION]
        if url_base is None:
            self[self.DOWNLOADS_PER_SESSION] = self.default_prefs[self.DOWNLOADS_PER_SESSION]
            self.save()


    def _init_defaults(self):
        self.default_prefs = {}
        self.default_prefs[self.URLBASE] = 'http://aldiko.beam-ebooks.de/'
        self.default_prefs[self.ACCOUNTS] = {}
        self.default_prefs[self.DOWNLOADS_PER_SESSION] = 10


    def _migrate_config_if_required(self):
        # Contains code for migrating versions of json schema
        # Make sure we store our schema version in the file
        schema_version = plugin_prefs.get(SCHEMA_VERSION, 0)
        if schema_version != DEFAULT_SCHEMA_VERSION:
            plugin_prefs[SCHEMA_VERSION] = DEFAULT_SCHEMA_VERSION
            # And now, do some migration stuff...

    def _get_db(self):
        if self.passed_db:
            return self.passed_db
        else:
            # In the GUI plugin we want current db so we detect when
            # it's changed.  CLI plugin calls need to pass db in.
            return get_gui().current_db


    def _get_prefs(self):
        return self.plugin_prefs


    def __getitem__(self, k):
        prefs = self._get_prefs()
        if k in prefs:
            return prefs[k]
        else:
            return None


    def __setitem__(self, k, v):
        prefs = self._get_prefs()
        prefs[k]=v


    def get_library_uuid(self):
        try:
            library_uuid = self._get_db().library_id
        except:
            library_uuid = ''
        return library_uuid


    def save(self):
        print "Saving myself"
        plugin_prefs.commit()
