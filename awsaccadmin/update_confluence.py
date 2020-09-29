import requests
import json
import getpass
import keyring
import re
import pandas as pd
from html_table_parser import HTMLTableParser

# Allow HTTPS connections with self-signed cert
requests.packages.urllib3.disable_warnings()

# Create login session for Confluence
# auth = ('mylogin', getpass.getpass())
s = requests.Session()
s.verify = False
s.headers = {"Content-Type": "application/json"}

page_id = 35192889


WIKI = "http://confluence.bgchtest.info/rest/api/"
BASE_URL = "https://confluence.bgchtest.info/rest/api/content"
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

def get_page_info(auth, page_id):
    url = '{base}/{pageid}'.format(base = BASE_URL,
                                   pageid = page_id)
    r = requests.get(url, auth = auth)
    r.raise_for_status()

    return r.json()

def get_page_ancestors(auth, page_id):
    # Get basic page information plus the ancestors property
    url = '{base}/{pageid}?expand=ancestors'.format(
        base = BASE_URL,
        pageid = page_id)
    r = requests.get(url, auth = auth)
    r.raise_for_status()
    return r.json()['ancestors']

# Retrieving page data
def get_data(auth, page_id):
    s.auth = auth
    r = s.get('{}content/{}'.format(WIKI, page_id),
              params = dict(expand='body.storage'))
    jr = r.json()
    content = jr['body']['storage'].get('value')
    return content

def get_page_content(auth, pageid):
    s.auth = auth

    url = '{base}/{pageid}?expand=body.storage'.format(
        base = BASE_URL,
        pageid = pageid)
    r = s.get(url, auth=auth)
    # r = requests.get(url, auth = auth)
    r.raise_for_status()

    return (r.json()['body']['storage']['value'])

def get_words(auth, page_id):
    s.auth = auth
    comments = []
    r = s.get(
      '{}content/{}'.format(WIKI, page_id),
        params = dict(
           expand='body.storage'
           )
        )
    jr = r.json()
    # content = jr['body']['storage'].get('value')
    for cmnt in r: # No valid json, so we scan the result
        comments.append(cmnt) # Collect all strings into a list
        bytes = [] #Results are encoded, store decoded data in a list
        for byte in comments:
            byted = byte.decode('utf-8', 'ignore') #Decode as UTF-8 and ignore errors
            bytes.append(byted)
    bytesstr = "".join(bytes) # List contains split strings, join them together into a single line
    parsed = json.loads(bytesstr); # Convert the line into a valid JSON object
    pgdataval = parsed['body']['storage'].get('value') # Retrieving text from the page
    return jr, pgdataval

def get_header_body_data_as_lists(data):
    p = HTMLTableParser()
    p.feed(data)
    # print(p.tables)
    accheaders = p.tables[0][0]
    accdata = p.tables[0][1:]
    return accheaders, accdata

def put_page_body(auth, page_id, postdata):
    s.auth = auth
    headers = {
        'Accept': 'application/json' ,
        'Content-Type': 'application/json'  }
    url = '{base}/{pageid}'.format(base=BASE_URL,pageid=page_id)

    r = s.put(url,
               data = postdata,
               auth = auth,
               headers=headers)
    # print(f"Req returned {r}")
    return r

def form_new_page(auth, page_id, page_html):
    info = get_page_info(auth, page_id)
    ver = int(info['version']['number']) + 1
    ancestors = get_page_ancestors(auth, page_id)

    anc = ancestors[-1]
    del anc['_links']
    del anc['_expandable']
    del anc['extensions']


    newpagebody = {
        'id': page_id,
        'type': 'page',
        'title': info['title'],
        'ancestors': [anc],
        'body': {
            'storage': {
                'value': str(page_html),
                'representation': 'storage',
            }
        },
        'version': {'number': ver}
    }

    return json.dumps(newpagebody)

def go():
    auth = get_login()
    # pagebody, data = get_words(auth, page_id)
    data = get_page_content(auth, page_id)

    accheaders, accdata = get_header_body_data_as_lists(data)

    print(accheaders)
    print(accdata)
    # enc_para = '<p class="auto-cursor-target"><br /></p>'
    #
    # page_html = '<p class="auto-cursor-target"><br /></p><table><colgroup><col /><col /><col /><col /><col /><col /><col /><col /><col /><col /><col /></colgroup><tbody><tr><th>AccountDebsNumber</th><th>AccountName</th><th>AccountOwner</th><th colspan="1">Active</th><th colspan="1">Description</th><th colspan="1">OwnerTeam</th><th colspan="1">PreviousName</th><th colspan="1">RealUsers</th><th colspan="1">SecOpsEmail</th><th colspan="1">SecOpsSlackChannel</th><th colspan="1">TeamEmail</th></tr><tr><td><p class="p1"><span class="s1">01234567810</span></p></td><td><p class="p1"><span class="s1">DebsTestAccount2</span></p></td><td>Deborah Balm</td><td colspan="1">Y</td><td colspan="1"><p class="p1"><span class="s1">Debs purple Test Account 2</span></p></td><td colspan="1">SRE2</td><td colspan="1">Debs</td><td colspan="1">N</td><td colspan="1"><p class="p1"><span class="s1"><a href="mailto:secadmin-prod.awsnotifications@hivehome.dev">secadmin-prod.awsnotifications@hivehome.dev</a></span></p></td><td colspan="1"><p class="p1"><span class="s1">#debs_backoffice</span></p></td><td colspan="1"><p class="p1"><span class="s1"><a href="mailto:sre@bgch.co.uk">sre@bgch.co.uk</a></span></p></td></tr><tr><td colspan="1">9849534589</td><td colspan="1"><span class="s1">Chris54Account</span></td><td colspan="1">Chris Allison</td><td colspan="1">Y</td><td colspan="1">Chris Allisons Account</td><td colspan="1">SRE2</td><td colspan="1">Chris</td><td colspan="1">N</td><td colspan="1"><p class="p1"><span class="s1"><a href="mailto:secadmin-prod.awsnotifications@hivehome.dev">secadmin-prod.awsnotifications@hivehome.dev</a></span></p></td><td colspan="1"><p class="p1"><span class="s1">#debs_backoffice</span></p></td><td colspan="1"><p class="p1"><span class="s1"><a href="mailto:sre@bgch.co.uk">sre@bgch.co.uk</a></span></p></td></tr></tbody></table><p class="auto-cursor-target"><br /></p>'
    # table_html = re.sub(enc_para,'',page_html)
    #
    # print(table_html)

    df_marks = pd.DataFrame({'name': [ 'Somu','Kiku','Amol','Lini' ],
                             'physics': [ 68,74,77,78 ],
                             'chemistry': [ 84,56,73,69 ],
                             'algebra': [ 78,88,82,87 ]})

    # render dataframe as html
    html = df_marks.to_html()
    print(html)

    # postdata = form_new_page(auth, page_id,page_html)
    # response = put_page_body(auth, page_id, postdata)
    #
    # if response.status_code == 200:
    #     print("RESPONSE ALL GOOD")
    # else:
    #     print(response.status_code)
    #     print(response.content)
    #     print(response.text)



go()