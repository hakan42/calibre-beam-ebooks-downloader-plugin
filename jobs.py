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


from calibre_plugins.beam_ebooks_downloader.prefs import PrefsFacade
from calibre_plugins.beam_ebooks_downloader.adder import EBookAdder
from calibre_plugins.beam_ebooks_downloader.downloader import BeamEbooksDownloader
from calibre_plugins.beam_ebooks_downloader.urlnorm import norms


def do_mirror(cpus, account, notification=lambda x, y:x):
    print "do_mirror in jobs.py"

    print "Account is: %s" % (account)

    # This server is an arbitrary_n job, so there is a notifier available.
    # Set the % complete to a small number to avoid the 'unavailable' indicator
    notification(0.01, "Starting up...")

    from calibre.library import db
    from calibre.utils.config import prefs
    prefs.refresh()
    db = db(read_only=False)

    print "DB is: %s" % (db)

    prefs = PrefsFacade(db)
    print "Prefs are: %s" % (prefs)
    print "Library id is (%s)" % (prefs.get_library_uuid())

    reporter = ConsoleReporter()
    downloader = BeamEbooksDownloader(prefs, caller = reporter)
    print "-- LALA -- Downloader is: %s" % (downloader)

    if account[prefs.ENABLED]:
        downloader.login(account)

        if downloader.successful_login == False:
            notification(1.00, "Failed to log in...")
        else:
            notification(0.05, "Parsing document tree now...")
            downloadable_ebooks = downloader.recursive_descent(norms(prefs[prefs.URLBASE]))
            notification(0.50, "Loaded OPDS pages")
            reporter.notify(downloadable_ebooks)
            #
            # Now, download the obtained ebooks...

    notification(1.00, "Done...")

    adder = EBookAdder(prefs, "beam-ebooks")

    adder.load_books()

    new_ebooks = []

    for entry in downloadable_ebooks:
        beamebooks_id = entry['id']

        book = adder.books_of_this_shop.get(beamebooks_id)
        if book is None:
            new_ebooks.append(entry)

    result = (new_ebooks)

    return result


class ConsoleReporter(object):

    def __init__(self):
        pass

    def notify(self, message = None):
        if message is not None:
            print "Notified of: %s" % (message)
