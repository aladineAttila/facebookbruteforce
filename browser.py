#!/usr/bin/env python2
import mechanize
import random
import cookielib

useragents = ['Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1']


class Browser(mechanize.Browser):
    def __init__(self):
        mechanize.Browser.__init__(self)
        self.cj = cookielib.LWPCookieJar()
        self.set_handle_robots(False)
        self.set_handle_redirect(True)
        self.set_cookiejar(self.cj)
        self.set_handle_equiv(True)
        self.set_handle_referer(True)
        self.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.addheaders = [('User-agent', random.choice(useragents))]

    def request_from(self, url, form):
        self.open(url)
        self.select_form(nr = 0)
        for f in form:
            self.form[f] = form[f]
        self.submit()
        return self.geturl()
