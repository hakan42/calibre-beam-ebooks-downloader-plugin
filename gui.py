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


from PyQt4.Qt import (Qt, QDialog, QWidget, QGridLayout, QLabel, QLineEdit)


class DownloadDialog(QWidget):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config
