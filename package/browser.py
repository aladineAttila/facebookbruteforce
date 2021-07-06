#!/usr/bin/env python2
import mechanize
import random
import cookielib
import pprint

useragents = ['Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1']

class Browser:
	def __init__(self):
		self.br = mechanize.Browser()
		self.cj = cookielib.LWPCookieJar()
		self.br.set_handle_robots(False)
		self.br.set_handle_redirect(True)
		self.br.set_cookiejar(self.cj)
		self.br.set_handle_equiv(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	
	def login(self, url, user_form, user_id, password_form, password):
		agent = random.choice(useragents)
		self.br.addheaders = [('User-agent', agent)]
		self.br.open(url)
		self.br.select_form(nr = 0)
		self.br.form['{0}'.format(user_form)] = user_id
		self.br.form['{0}'.format(password_form)] = password
		self.br.submit()
		return self.br.geturl(), self.br.response().read()

if __name__== "__main__":
	result = (Browser().login("https://www.facebook.com", "xxxxxxxxxxxx", "xxxxxxxxxxx"))
	pprint.pprint(result[1])

