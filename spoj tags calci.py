import sys
import socket
from time import sleep
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
    sys.exit(1)

br = Browser()

br.addheaders = [('connection', 'keep-alive'), ('Host', 'stackoverflow.com'),
    ('Referer', 'https://www.google.co.in/'), ('Upgrade-Insecure-Requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
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

total = len(solved)
if total is 0:
    print "You have not solved any problem successfully!\n"
    sys.exit(1)

print '\n%s solved problems found.\n' % str(total)

print 'Processing tags...\n'

for i in range(len(solved)):
    x = (float(i)/(total-1)) * 100
    url = "http://www.spoj.com/problems/"+solved[i]

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

    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('=' * (int(x/5.0)), x))
    sys.stdout.flush()
print '\n'

tags_length = []
for tag in tags.keys():
    tags_length.append((tag, len(tags[tag])))
if 'no_tag' in globals() or 'no_tag' in locals():
    tags_length.append(('Non-tageed', len(no_tag)))

tags_length.sort(reverse=True, key=lambda tup: tup[1])

prelink = 'http://www.spoj.com/problems/'
for k,v in tags.iteritems():
    print k.upper()
    for i in range(len(v)):
        url = prelink + v[i]
        print url + '\n'

class TreeViewFilterWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Spoj Tags Frequency Calculator")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.tags_lengthstore = Gtk.ListStore(str, int)
        for each in tags_length:
            self.tags_lengthstore.append(list(each))

        self.language_filter = self.tags_lengthstore.filter_new()

        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Tags", "Number of Problems"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        self.buttons = list()
        for btn in ["Exit"]:
            button = Gtk.Button(btn)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 9, 7)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def on_selection_button_clicked(self, widget):
        Gtk.main_quit()

win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
