import sys
import socket

REMOTE_SERVER = "http://www.google.com/"
def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
if(not is_connected()):
    print "\nNo Internet Connection Found!\n"
    sys.exit(1)

try:
    from mechanize import Browser
except ImportError:
    print "\nmechanize not installed, please install using :\npip install mechanize\n"
    sys.exit(1)

br = Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
          rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)

br.open("http://www.spoj.com/")

# br.select_form
