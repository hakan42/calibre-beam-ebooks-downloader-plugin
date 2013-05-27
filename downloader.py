#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__ = 'Apache License, Version 2.0'
__copyright__ = '2013, Hakan Tandogan <hakan at gurkensalat.com>'
__docformat__ = 'restructuredtext en'


#
import urllib2
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

        self.browser = Browser(enable_developer_tools=True)

    def login(self):
        url  = self.urlbase + "/aldiko/cookisetzen.php"
        print "  URL: '%s'" % (url)
        
        print "Browser: '%s'" % (self.browser)
        print "    UA : '%s'" % (self.browser.user_agent)

        self.browser.visit(url)

        # print "Content: '%s'" % (self.browser.html)

        soup = BeautifulSoup(self.browser.html)
        # print "Soup: '%s'" % (soup)

        form = self.browser.select_form(nr = 0)
        print "Form: '%s'" % (form)
        print "  Auth: '%s', '%s'" % (self.username, self.password)
        form['user'] = self.username
        form['pass'] = self.password
        self.browser.submit()

        print "New Content: '%s'" % (self.browser.html)

        soup = BeautifulSoup(self.browser.html)
        print "New Soup: '%s'" % (soup)

        print "Cookies: '%s'" % (self.browser.cookies)
