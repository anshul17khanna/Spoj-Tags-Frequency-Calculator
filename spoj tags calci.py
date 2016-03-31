import sys

try:
    from mechanize import Browser
except ImportError:
    print "mechanize not installed, please install using :\npip install mechanize\n"
    sys.exit(1)

br = Browser()
br.open("http://www.spoj.com/")

# br.select_form
