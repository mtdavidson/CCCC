import urllib2
import sys
import re

from BeautifulSoup import BeautifulSoup

import sqlite3
conn = sqlite3.connect('cards.db')
c = conn.cursor()

if (len(sys.argv) != 2):
    quit ('Please provide card id')

#TODO: Check ID Valid Format
page = urllib2.urlopen('http://www.koolkingdom.co.uk/acatalog/info_' + str(sys.argv [1]) + '.html').read();
#TODO: Check not 404
soup = BeautifulSoup(page)
soup.prettify()

#TODO: Clean price
cardName = soup.title.string
price = soup.find('actinic:prices').i.string
price = re.sub('[^0123456789\.]', '', price)

print str (sys.argv [1]) + " " + cardName + " " + price;

#TODO: Get card name

#TODO: Add result to file [sqlite]
