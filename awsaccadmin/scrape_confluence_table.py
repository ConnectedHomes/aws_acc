import requests
import json
import getpass
import keyring
import re
import html
from lxml import etree, html
from IPython.display import display_html
import pandas as pd
from datetime import datetime

from html_table_parser import HTMLTableParser

# Allow HTTPS connections with self-signed cert
requests.packages.urllib3.disable_warnings()

# Create login session for Confluence
# auth = ('mylogin', getpass.getpass())
s = requests.Session()
s.verify = False
s.headers = {"Content-Type": "application/json"}

page_id = 35192889
# pageid = 2229576

WIKI = "http://confluence.bgchtest.info/rest/api/"
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

# def read_page(auth, pageid):
#     url = '{base}/{pageid}?expand=body.storage'.format(base = BASE_URL,
#                                    pageid = pageid)
#     r = requests.get(url, auth = auth)
#     r.raise_for_status()
#     return r.json()

# Obtain text from Confluence HTML layout


# Retrieving page data
def get_data(auth, page_id):
    s.auth = auth
    r = s.get('{}content/{}'.format(WIKI, page_id),
              params = dict(expand='body.storage'))
    jr = r.json()
    content = jr['body']['storage'].get('value')
    return content

def get_words(auth, page_id):
    s.auth = auth
    comments = []
    r = s.get(
      '{}content/{}'.format(WIKI, page_id),
        params = dict(
           expand='body.storage'
           )
        )
    for cmnt in r: # No valid json, so we scan the result
        comments.append(cmnt) # Collect all strings into a list
        bytes = [] #Results are encoded, store decoded data in a list
        for byte in comments:
            byted = byte.decode('utf-8', 'ignore') #Decode as UTF-8 and ignore errors
            bytes.append(byted)
    bytesstr = "".join(bytes) # List contains split strings, join them together into a single line
    parsed = json.loads(bytesstr); # Convert the line into a valid JSON object
    pgdataval = parsed['body']['storage'].get('value') # Retrieving text from the page
    return pgdataval


def go():
    auth = get_login()
    data2 = get_words(auth, page_id)
    # print(data2)

    p = HTMLTableParser()
    p.feed(data2)
    print(p.tables)


go()