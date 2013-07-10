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


from PyQt4.Qt import (Qt, QDialog, QWidget, QGridLayout, QVBoxLayout, QPushButton,
                      QLabel, QLineEdit, QMessageBox, QTextEdit)

from calibre.gui2 import Dispatcher
from calibre.gui2.ui import get_gui
from calibre_plugins.beam_ebooks_downloader import Downloader
from calibre_plugins.beam_ebooks_downloader.prefs import PrefsFacade
from calibre_plugins.beam_ebooks_downloader.downloader import BeamEbooksDownloader
from calibre_plugins.beam_ebooks_downloader.urlnorm import norms


class DownloadDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI
        self.db = gui.current_db

        self.prefs = PrefsFacade(self.db)

        self.version = Downloader.version

        # The GUI, created and layouted by hand...
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setWindowTitle('Beam EBooks Downloader')
        self.setWindowIcon(icon)

        self.log_area = QTextEdit('Log output', self)
        self.log_area.setReadOnly(True)
        self.log_area.setLineWrapMode(QTextEdit.NoWrap);
        self.log_area.setText("")
        self.layout.addWidget(self.log_area)

        self.download_button = QPushButton('Download books', self)
        self.download_button.clicked.connect(self.download)
        self.layout.addWidget(self.download_button)

        self.conf_button = QPushButton('Configure this plugin', self)
        self.conf_button.clicked.connect(self.config)
        self.layout.addWidget(self.conf_button)

        self.resize(self.sizeHint())


    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        # Not necessary, the downloader will obtain fresh config anyway...
        # self.label.setText(prefs['hello_world_msg'])


    def notify(self, message = None):
        if message is not None:
            # insertPlainText inserts at the beginning of the log area...
            self.log_area.append(message)
            sb = self.log_area.verticalScrollBar()
            sb.setValue(sb.maximum())


    def download(self):
        prefs = self.prefs

        self.download_button.setEnabled(False)
        self.conf_button.setEnabled(False)

        downloader = BeamEbooksDownloader(self.prefs, self.version, caller = self)
        self.notify("Downloader is: %s" % (downloader))

        # Loop over all accounts until we have support for selection
        for account_id in prefs[prefs.ACCOUNTS]:
            account = prefs[prefs.ACCOUNTS][account_id]
            account[prefs.ACCOUNT_ID] = account_id

            if account[prefs.ENABLED]:
                self.enqueue(account, downloader)

        self.hide()


    def enqueue(self, account, downloader):
        prefs = self.prefs

        self.notify("Account: '%s'" % account[prefs.USERNAME])
        # downloader.login(account)

        func = 'arbitrary_n'
        # func = 'arbitrary'
        cpus = self.gui.job_manager.server.pool_size
        print "CPUs: %s" % (cpus)
        args = ['calibre_plugins.beam_ebooks_downloader.jobs', 'do_mirror', (cpus, account)]
        desc = 'Beam EBooks Downloader'
        job = self.gui.job_manager.run_job(Dispatcher(self._done), func, args=args, description=desc)
        print "Job: %s" % (job)

        self.notify("  Start parsing OPDS catalog")

        # if downloader.successful_login == False:
        #     self.notify("Failed to log in...")
        # else:
        #     self.notify("Scanning (beam) private library now...")
        #     downloader.recursive_descent(norms(prefs[prefs.URLBASE]))

    def _done(self, job):
        print "Done Downloading"
        print "Self: %s" % (self)
        print "Job: %s" % (job)
        # print "  Result: %s" % (job.result)
        # print "  Result: %s" % (len(job.result))
        self.notify("  Finished download catalog...")

        if job.result is not None:
            for entry in job.result:
                beamebooks_id = entry['id']
                message = "<br/>Ebook # %s" % (beamebooks_id)
                self.notify(message)

        self.download_button.setEnabled(True)
        self.conf_button.setEnabled(True)

        payload = job.result
        msg = "Parsing OPDS Catalog complete, found %s ebooks." % (len(job.result))
        msg = msg + "<br>Do you want to import the books into the library?"

        # question_dialog
        self.gui.proceed_question(self._add_ebooks, payload, job.details,
                    'OPDS Download Log', 'OPDS parse complete', msg, show_copy_button = False)


    def _add_ebooks(self, payload):
        print "Done Downloading, Step 2"
        print "Self: %s" % (self)
        # print "Payload: %s" % (payload)
        # Printing the complete payload at once gives [IOError 12] - Out of space (memory, that is...)
        self.notify("  Finished adding books...")
        for entry in payload:
            print "Entry: %s" % entry
