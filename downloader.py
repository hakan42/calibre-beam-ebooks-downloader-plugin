#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


#
import re
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.jsbrowser.browser import Browser

#
class BeamEbooksDownloader():

    def __init__(self):
        print "Initializing BeamEbooksDownloader()"
        print "  myself: '%s'" % (self)

        from calibre_plugins.beam_ebooks_downloader.prefs import prefs

        self.urlbase  = prefs.__getitem__(prefs.URLBASE)
        self.username = prefs.__getitem__(prefs.USERNAME)
        self.password = prefs.__getitem__(prefs.PASSWORD)

        self.beamid = None
        self.successful_login = False

        self.already_visited_links = []

        self.browser = Browser(enable_developer_tools=True)

    def login(self):
        self.beamid = None
        self.successful_login = False

        self.already_visited_links = []

        url  = self.urlbase + "/aldiko/cookisetzen.php"
        print "  URL: '%s'" % (url)
        
        print "Browser: '%s'" % (self.browser)
        print "    UA : '%s'" % (self.browser.user_agent)

        self.browser.visit(url)

        # print "Content: '%s'" % (self.browser.html)

        # soup = BeautifulSoup(self.browser.html)
        # print "Soup: '%s'" % (soup)

        form = self.browser.select_form(nr = 0)
        print "Form: '%s'" % (form)
        print "  Auth: '%s', '%s'" % (self.username, self.password)
        form['user'] = self.username
        form['pass'] = self.password
        self.browser.submit()

        # print "New Content: '%s'" % (self.browser.html)
        # soup = BeautifulSoup(self.browser.html)
        # print "New Soup: '%s'" % (soup)

        # print "Cookies: '%s'" % (self.browser.cookies)
        for cookie in self.browser.cookies:
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

        self.browser.visit(url)
        soup = BeautifulSoup(self.browser.html)
        print "Soup: '%s'" % (soup)

        links_to_visit = []

        entrylist = soup.findAll('entry')
        for entry in entrylist:
            # print "  Entry: '%s'" % (entry)
            # print "\n"
            linklist = entry.findAll('link', href = True)
            for link in linklist:
                print "\n"
                print "    Link: '%s'" % (link)
                href = link['href']
                print "      HRef: '%s'" % (href)

                match = re.search('\.png$', href)
                if match: 
                    continue

                match = re.search('\.jpg$', href)
                if match:
                    continue

                match = re.search('\/about\.php$', href)
                if match: 
                    continue

                match = re.search('\/kategorien\.xml$', href)
                if match: 
                    continue

                match = re.search('\/xmlcatalog\.php5\?.*$', href)
                if match:
                    continue

                match = re.search('\/download\.php5\?.*$', href)
                if match: 
                    continue

                print "        Seems to be a followable link ('%s')" % (href)
                links_to_visit.append(href)

        # Finally, visit all pages that we encountered
        if further_descend:
            for link in links_to_visit:
                self.recursive_descent(link)
