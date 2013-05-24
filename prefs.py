#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


from calibre.utils.config import JSONConfig

STORE_SCHEMA_VERSION = 'SchemaVersion'
DEFAULT_SCHEMA_VERSION = 1.0

# This is where all preferences for this plugin will be stored
plugin_prefs = JSONConfig('plugins/Beam EBooks Downloader')

# Set defaults
plugin_prefs.defaults['hello_world_msg'] = 'Hello, World!'


def migrate_config_if_required():
    # Contains code for migrating versions of json schema
    # Make sure we store our schema version in the file
    schema_version = plugin_prefs.get(STORE_SCHEMA_VERSION, 0)
    if schema_version != DEFAULT_SCHEMA_VERSION:
        plugin_prefs[STORE_SCHEMA_VERSION] = DEFAULT_SCHEMA_VERSION


class PrefsFacade():

    def __init__(self, passed_db=None):
        self.default_prefs = plugin_prefs.defaults
        self.libraryid = None
        self.plugin_prefs = plugin_prefs
        self.passed_db = passed_db


    def save(self):
        print "Saving myself"
        plugin_prefs.commit()


# Ensure our config gets migrated
migrate_config_if_required()

# Return myself
prefs = PrefsFacade()
