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
from calibre.gui2.actions import InterfaceAction
from calibre_plugins.beam_ebooks_downloader.gui import DownloadDialog


class BeamEbooksDownloaderAction(InterfaceAction):

    action_spec = ('Beam EBooks Downloader', None, 'Run the Beam Ebooks Downloader', None)

    def genesis(self):
        # This method is called once per plugin, do initial setup here
        icon = get_icons('images/icon.png')

        # The qaction is automatically created from the action_spec defined above
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        # The base plugin object defined in __init__.py
        base_plugin_object = self.interface_action_base_plugin

        do_user_config = base_plugin_object.do_user_config

        d = DownloadDialog(self.gui, self.qaction.icon(), do_user_config)
        d.show()

    def apply_settings(self):

        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        pass
