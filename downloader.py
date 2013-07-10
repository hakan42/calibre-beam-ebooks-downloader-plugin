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
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre import browser
from calibre_plugins.beam_ebooks_downloader.adder import EBookAdder
from calibre_plugins.beam_ebooks_downloader.urlnorm import norms

#
class BeamEbooksDownloader():

    def __init__(self, prefs, version = None, caller = None):
        print "Initializing BeamEbooksDownloader()"
        print "  myself: '%s'" % (self)

        self.prefs = prefs
        self.urlbase  = prefs[prefs.URLBASE]

        if version is None:
            from calibre_plugins.beam_ebooks_downloader import Downloader
            version = Downloader.version

        self.caller = caller

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

    def save_response(self, response):
        if not os.path.exists(self.tempdirpath):
            os.makedirs(self.tempdirpath)

        try:
            filename = '%s/response-%s-%d.txt' % (self.tempdirpath, self.account_id, self.filenumber)
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

    def login(self, account):
        self.beamid = None
        self.successful_login = False

        self.already_visited_links = []
        self.downloadable_ebooks = []

        self.account_id = account[self.prefs.ACCOUNT_ID]

        self.username = account[self.prefs.USERNAME]
        self.password = self.prefs.decrypt_password(account[self.prefs.OBFUSCATED_PASSWORD])

        # Remove all cookies to be extra safe
        self.browser.cookiejar.clear()
        self.filenumber = 1000

        if self.caller is not None:
            self.caller.notify("Logging in")

        url = self.urlbase + "/aldiko/cookisetzen.php"
        url = norms(url)
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
                        self.caller.notify("Login Successful")

        # print "Beam ID: '%s', '%s'" % (self.beamid, self.successful_login)

    def recursive_descent(self, absolute_url = None, further_descend = True):
        if absolute_url is None:
            url  = self.urlbase
        else:
            url  = absolute_url

        caller = self.caller

        url = norms(url)
        if url in self.already_visited_links:
            print "Already have been here ('%s')..." % (url)
        else:
            harvested_urls = self.prefs[self.prefs.HARVESTED_URLS]
            harvest_state = harvested_urls.get(url)
            if harvest_state is None:
                harvest_state = {}
                self.prefs[self.prefs.HARVESTED_URLS][url] = harvest_state
                self.prefs.save()

            status = harvest_state.get(self.prefs.HARVEST_STATE)
            if status is None:
                harvest_state[self.prefs.HARVEST_STATE] = self.prefs.HARVEST_STATE_REVISIT
                self.prefs.save()

            title = harvest_state.get(self.prefs.HARVEST_TITLE)
            if title is None:
                harvest_state[self.prefs.HARVEST_TITLE] = ""
                self.prefs.save()

            if caller is not None:
                caller.notify("Visiting ('%s', '%s')..." % (url, harvest_state))

            self.visit_url(absolute_url, further_descend)

        # In any case, return a list of ebooks to download
        return self.downloadable_ebooks

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
                        href = norms(href)
                        print "          Seems to be a followable link ('%s')" % (href)
                        links_to_visit.append(href)

                match = re.match('urn:beam-ebooks:alle', contents)
                if match:
                    href = self.extract_link(entry)
                    if href:
                        href = norms(href)
                        print "          Seems to be a followable link ('%s')" % (href)
                        links_to_visit.append(href)

                match = re.match('urn:beam-ebooks:titelnr:', contents)
                if match:
                    (href, mimetype) = self.extract_link(entry)
                    if href:
                        href = norms(href)
                        match = re.search('\/download\.php5\?.*$', href)
                        if match:
                            print "          Seems to be an ebook ('%s', '%s')" % (mimetype, href)
                            data = {}
                            data['urn']      = contents
                            data['href']     = href
                            data['mimetype'] = mimetype

                            foo = re.split(':', contents)
                            data['id'] = foo[3]

                            self.downloadable_ebooks.append(data)
                        else:
                            print "          Seems to be a followable link ('%s')" % (href)
                            links_to_visit.append(href)

        # Finally, visit all pages that we encountered
        if further_descend:
            for link in links_to_visit:
                link = norms(link)
                self.recursive_descent(link)

        # In any case, return the links we had to visit...
        return links_to_visit

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

        caller = self.caller

        adder = EBookAdder(self.prefs, "beam-ebooks")

        adder.load_books()

        handled_ebooks = 0
        for entry in self.downloadable_ebooks:

            urn = entry['urn']
            href = entry['href']
            mimetype = entry['mimetype']

            foo = re.split(':', urn)
            beamebooks_id = foo[3]

            book = adder.books_of_this_shop.get(beamebooks_id)
            if book is None:
                # Book not found, fetch and try to store in into the database
                if handled_ebooks < self.prefs[self.prefs.DOWNLOADS_PER_SESSION]:
                    handled_ebooks = handled_ebooks + 1
                    # Still in quota for this run
                    if caller is not None:
                        caller.notify("Working on book %d: %s" % (handled_ebooks, beamebooks_id))

                    if mimetype == 'application/epub+zip':
                        ext = 'epub'
                    else:
                        ext = 'bin'

                    path = self.tempdirpath + "/" + beamebooks_id + "." + ext
                    if os.path.exists(path) == False:
                        print "Have to download %s, %s, %s" % (beamebooks_id, mimetype, href)
                        self.browser.retrieve(href, path)

                    adder.add(path, beamebooks_id)

                else:
                    continue

        if caller is not None:
            caller.notify("Handled (%d of %d) books, waiting for next run" % (handled_ebooks, len(self.downloadable_ebooks)))
