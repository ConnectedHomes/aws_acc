import argparse
import getpass
import sys

import json
import keyring
import requests

#-----------------------------------------------------------------------------
# Globals

BASE_URL = "http://confluence.bgchtest.info/rest/api/content"
VIEW_URL = "http://confluence.bgchtest.info/pages/viewpage.action?pageId="


def get_login(username = None):
    ###Get the password for username out of the keyring.
    if username is None:
        username = getpass.getuser()

    passwd = keyring.get_password('confluence_script', username)

    if passwd is None:
        passwd = getpass.getpass()
        keyring.set_password('confluence_script', username, passwd)

    return (username, passwd)

def get_page_info(auth, pageid):
    url = '{base}/{pageid}'.format(base = BASE_URL,
                                   pageid = pageid)
    r = requests.get(url, auth = auth)
    r.raise_for_status()

    return r.json()

def read_page(auth, pageid):
    url = '{base}/{pageid}?expand=body.storage'.format(base = BASE_URL,
                                   pageid = pageid)
    r = requests.get(url, auth = auth)
    r.raise_for_status()
    return r.json()

def go():
    pageid = 35192889
    # pageid = 2229576

    auth = get_login()
    pageinfo = read_page(auth, pageid)
    print(pageinfo['title'])
    print(pageinfo['body'])


go()