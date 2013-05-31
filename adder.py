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


#
import re
import os
import sys
import zipfile
from calibre.ebooks.metadata.meta import metadata_from_formats


#
class EBookAdder():
    
    def __init__(self, prefs, indentifier_name = None):
        print "Initializing EBookAdder()"
        print "  myself: '%s'" % (self)

        self.prefs = prefs
        self.db = self.prefs._get_db()
        self.indentifier_name = indentifier_name

    def add(self, path = None, identifier = None):

        db = self.db
        print "Library database object is (%s)" % (db)

        # If file is not a correct zip, something went wrong, so continue with next file
        with zipfile.ZipFile(path, 'r') as zipf:
            if zipf.testzip() is not None:
                os.remove(path)
                pass

        # Now we know that the ebook is cached locally and is a valid zip file...
        print "Book Path: %s" % (path)
        formats = [ path ]
        print "  Formats: %s" % (formats)
        mi = metadata_from_formats(formats)
        print "    Obtained Metadata: %s" % (mi)

        internal_book_id = None 
        if db.has_book(mi):
            print "      Book already available in DB, would have to enhance with %s id %s" % (self.indentifier_name, identifier)
            book_ids = db.books_with_same_title(mi)
            print "        books_with_same_title: %s" % (book_ids)
            # Now, we should iterate over all books and try to match author as well....
            # Well, next time :-)
            try:
                internal_book_id = book_ids.pop()
                print "        ID of pre-existing book: %s" % (internal_book_id)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                pass
        else:
            print "      New Book, trying to add it to database"
            internal_book_id = db.import_book(mi, formats)
            print "        ID of new book: %s" % (internal_book_id)

        if internal_book_id is not None:
            print "      Enhancing book #%s with %s id '%s'" % (internal_book_id, self.indentifier_name, identifier)
            identifiers = db.get_identifiers(internal_book_id, index_is_id=True)
            print "        Old Identifiers: %s" % (identifiers)
            identifiers[self.indentifier_name] = identifier
            db.set_identifiers(internal_book_id, identifiers, notify=True, commit=True)

            identifiers = db.get_identifiers(internal_book_id, index_is_id=True)
            print "        New Identifiers: %s" % (identifiers)
