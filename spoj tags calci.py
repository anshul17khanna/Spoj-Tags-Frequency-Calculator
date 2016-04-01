import sys
import socket

REMOTE_SERVER = "www.google.com"
def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False
if is_connected() is False:
    print "\nInternet Connection Required!\n"
    sys.exit(1)

try:
    from mechanize import Browser
except ImportError:
    print "\nmechanize not installed, please install using :\npip install mechanize\n"
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "\nbs4 not installed, please install using :\npip install beautifulsoup4\n"

br = Browser()

br.addheaders = [('connection', 'keep-alive'), ('Host', 'stackoverflow.com'),
    ('Referer', 'https://www.google.co.in/'), ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
]
br.set_handle_robots(False)

print "\nEnter Username : ",
username = raw_input()
url = "http://www.spoj.com/users/" + username
response = br.open(url)
verify = response.read()

if verify.find('@'+username) == -1:
    print "\nUsername does not exist!\n"
    sys.exit(1)

solved = []

soup = BeautifulSoup(verify, 'html.parser')
for table in soup.find_all('table', attrs={'class': 'table-condensed'}):
    for row in table.find_all('tr'):
        for item in row.find_all('td'):
            if item.get_text() != '':
                solved.append(item.get_text())

tags = {}

for i in range(len(solved)):
    url = "http://www.spoj.com/problems/"+solved[i]
    print url+'\n'
    response = br.open(url)

    find_tag = response.read()

    soup = BeautifulSoup(find_tag, 'html.parser')

    if find_tag.find("no tags") != -1:
        if 'no_tag' in globals() or 'no_tag' in locals():
            no_tag.append(solved[i])
        else:
            no_tag = []
            no_tag.append(solved[i])
    else:

        for get_tag in soup.find_all('span', attrs={'class': 'problem-tag'}):

            if get_tag.get_text() in tags.keys():
                tags[get_tag.get_text()].append(solved[i])
            else:
                tags[get_tag.get_text()] = []
                tags[get_tag.get_text()].append(solved[i])

tags_length = []
for tag in tags.keys():
    tags_length.append((tag, len(tags[tag])))

tags_length.sort(reverse=True, key=lambda tup: tup[1])

for tag in range(len(tags_length)):
    (a, b) = tags_length[tag]
    print a + ' : ' + str(b) + '\n'

if 'no_tag' in globals() or 'no_tag' in locals():
    print 'not tagged : ' + str(len(no_tag)) + '\n'



'''
from time import sleep
import sys

for i in range(21):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)
'''
