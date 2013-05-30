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
import os
import sys
import tempfile
import re
import zipfile
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre import browser

#
class BeamEbooksDownloader():

    def __init__(self, prefs, version):
        print "Initializing BeamEbooksDownloader()"
        print "  myself: '%s'" % (self)

        self.prefs = prefs

        self.urlbase  = prefs[prefs.URLBASE]
        self.username = prefs[prefs.USERNAME]
        self.password = prefs[prefs.PASSWORD]

        self.beamid = None
        self.successful_login = False

        self.already_visited_links = []

        self.downloadable_ebooks = []

        # TODO How do I access this string from the calibre core?
        USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101210 Gentoo Firefox/3.6.13'
        user_agent =  'calibre-beam-ebooks-downloader-plugin/%d.%d.%d' % (version)
        user_agent = USER_AGENT + ' ' + user_agent 
        self.browser = browser(user_agent=user_agent)
        # self.browser.set_debug_http(True)
        # self.browser.set_debug_responses(True)

        # self.tempdirpath = tempfile.mkdtemp(prefix = 'calibre-beam-ebooks-downloader-plugin-')
        self.tempdirpath = tempfile.gettempdir() + '/' + 'calibre-beam-ebooks-downloader-plugin'
        print "Saving stuff into '%s'" % (self.tempdirpath)

        self.filenumber = 1000

    def save_response(self, response):
        if not os.path.exists(self.tempdirpath):
            os.makedirs(self.tempdirpath)

        try:
            filename = '%s/response-%d.txt' % (self.tempdirpath, self.filenumber)
            self.filenumber = self.filenumber + 1

            f = open(filename, 'w')
            f.write("Response Code: '%s'" % (response.code))
            f.write("\n\n")

            content = response.get_data()
            f.write("Content: '%s'" % (content))
            f.write("\n\n")

            # soup = BeautifulSoup(self.browser.html)
            # print "New Soup: '%s'" % (soup)
            # f.write("\n\n")

            f.close()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            pass

    def login(self):
        self.beamid = None
        self.successful_login = False

        self.already_visited_links = []
        self.downloadable_ebooks = []

        url  = self.urlbase + "/aldiko/cookisetzen.php"
        print "  URL: '%s'" % (url)

        print "Browser: '%s'" % (self.browser)
        # print "    UA : '%s'" % (self.browser.user_agent)

        response = self.browser.open(url)
        self.save_response(response)

        print "Cookies: '%s'" % (self.browser.cookiejar)

        if response.code == 200:
            form = self.browser.select_form(nr = 0)
            print "Form: '%s'" % (form)
            print "  Auth: '%s', '%s'" % (self.username, self.password)
            self.browser.form['user'] = self.username
            self.browser.form['pass'] = self.password
            self.browser.submit()

        # After from submission
        self.save_response(response)
        # print "Response Code: '%s'" % (response.code)
        # print "Cookies: '%s'" % (self.browser.cookiejar)

        for cookie in self.browser.cookiejar:
            # print "  C: '%s'" % (cookie)
            if hasattr(cookie, 'name'):
                if hasattr(cookie, 'value'):
                    if cookie.name == 'beamid':
                        self.beamid = cookie.value
                        # TODO should we verify that the beamid is numeric???
                        self.successful_login = True

        print "Beam ID: '%s', '%s'" % (self.beamid, self.successful_login)

    def recursive_descent(self, absolute_url = None, further_descend = True):
        if absolute_url is None:
            url  = self.urlbase
        else:
            url  = absolute_url

        if url in self.already_visited_links:
            print "Already have been here ('%s')..." % (url)
        else:
            print "Visiting ('%s')..." % (url)
            self.visit_url(absolute_url, further_descend)

    def visit_url(self, url = None, further_descend = True):
        print "  URL: '%s'" % (url)

        self.browser.open(url)
        response = self.browser.open(url)
        self.save_response(response)
        
        content = response.get_data()
        soup = BeautifulSoup(content)
        # print "Soup: '%s'" % (soup)

        links_to_visit = []

        if response.code != 200:
            print "Something horrible happened (RC %s)" % (response.code)
            pass

        entrylist = soup.findAll('entry')
        for entry in entrylist:
            # print "  Entry: '%s'" % (entry)
            # print "\n"
            idtag = entry.find('id')
            if idtag is not None:
                # First element of list...
                contents = idtag.contents[0]
                print "    Id: '%s' / '%s'" % (idtag, contents)

                match = re.match('urn:beam-ebooks:private', contents)
                if match:
                    href = self.extract_link(entry)
                    if href:
                        print "          Seems to be a followable link ('%s')" % (href)
                        links_to_visit.append(href)

                match = re.match('urn:beam-ebooks:alle', contents)
                if match:
                    href = self.extract_link(entry)
                    if href:
                        print "          Seems to be a followable link ('%s')" % (href)
                        links_to_visit.append(href)

                match = re.match('urn:beam-ebooks:titelnr:', contents)
                if match:
                    (href, mimetype) = self.extract_link(entry)
                    if href:
                        match = re.search('\/download\.php5\?.*$', href)
                        if match:
                            print "          Seems to be an ebook ('%s', '%s')" % (mimetype, href)
                            data = {}
                            data['urn']      = contents
                            data['href']     = href
                            data['mimetype'] = mimetype
                            self.downloadable_ebooks.append(data)
                        else:
                            print "          Seems to be a followable link ('%s')" % (href)
                            links_to_visit.append(href)

        # Finally, visit all pages that we encountered
        if further_descend:
            for link in links_to_visit:
                self.recursive_descent(link)

    def extract_link(self, entry):
        linklist = entry.findAll('link', href = True, type = True)
        for link in linklist:
            href = link['href']
            mimetype = link['type']

            match = re.search('^image\/.*', mimetype)
            if match:
                continue

            print "      Link: '%s'" % (link)
            print "        HRef: '%s'" % (href)
            print "        Type: '%s'" % (mimetype)

            match = re.search('^http\:\/\/', href)
            if match is None:
                if re.search('\/aldiko\/', href) is None:
                    href = self.urlbase + '/aldiko/' + href
                else:
                    href = self.urlbase + href
                print "        Extentended HRef: '%s'" % (href)

            match = re.search('\/bibliothek\.php\?.*$', href)
            if match:
                return href

            match = re.search('\/bibuebersicht\.php5\?.*$', href)
            if match:
                return href

            match = re.search('\/pakete\.php5\?.*$', href)
            if match:
                return href

            match = re.search('\/download\.php5\?.*$', href)
            if match:
                return (href, mimetype)

            # Just relative links for packages 
            match = re.search('\/paket\.php5\?paketnr=.*$', href)
            if match:
                return (href, mimetype)

        return None

    # Now, mirror all ebooks encountered in the loop above
    def download_ebooks(self):

        print "Library id is (%s)" % (self.prefs.get_library_uuid())

        db = self.prefs._get_db()
        print "Library database object is (%s)" % (db)

        # Not sure if this is the most efficient way of finding books in the database...
        beam_books = {}
        data = db.get_data_as_dict()
        print "Library data is (%s)" % (db)
        for book in data:
            try:
                # print "\n"
                # print "  Data Item (%s)" % (book)
                # amazon:B0056ADMZE, beam-ebooks:19789, goodreads:11791889
                if book['identifiers'] is not None:
                    identifiers = re.split(',', book['identifiers'])
                    # print "    Identifiers: '%s'" % (identifiers)
                    for identifier in identifiers:
                        if re.match('^beam-ebooks\:', identifier):
                            beamebooks_id = re.split(':', identifier)[1]
                            # print "      Beam Ebooks ID: '%s'" % (beamebooks_id)
                            beam_books[beamebooks_id] = book
            except:
                pass

        print "\n"

        for book_id in beam_books:
            try:
                print "\n"
                print "  Beam EBook (%s, %s)" % (book_id, beam_books[book_id])
            except:
                pass

        handled_ebooks = 0
        for entry in self.downloadable_ebooks:

            urn = entry['urn']
            href = entry['href']
            mimetype = entry['mimetype']

            foo = re.split(':', urn)
            beamebooks_id = foo[3]
            # print "  x: (%s), id: %s" % (foo, beamebooks_id)

            if mimetype == 'application/epub+zip':
                ext = 'epub'
            else:
                ext = 'bin'

            path = self.tempdirpath + "/" + beamebooks_id + "." + ext
            if os.path.exists(path) == False:
                print "Have to download %s, %s, %s" % (beamebooks_id, mimetype, href)
                self.browser.retrieve(href, path)

            # If file is not a correct zip, something went wrong, so continue with next file
            with zipfile.ZipFile(path, 'r') as zipf:
                if zipf.testzip() is not None:
                    os.remove(path)
                    continue
