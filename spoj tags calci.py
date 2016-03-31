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
    print "\nNo Internet Connection!\n"
    sys.exit(1)

try:
    from mechanize import Browser
except ImportError:
    print "\nmechanize not installed, please install using :\npip install mechanize\n"
    sys.exit(1)

br = Browser()

br.addheaders = [('connection', 'keep-alive'), ('Host', 'stackoverflow.com'),
            ('Referer', 'https://www.google.co.in/'), ('Upgrade-Insecure-Requests', '1'),
            ('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
]
br.set_handle_robots(False)

br.open("http://www.google.com/")

# br.select_form
