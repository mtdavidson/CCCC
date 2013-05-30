import urllib2
import sys
import re
import sqlite3

from BeautifulSoup import BeautifulSoup

conn = sqlite3.connect('cards.sqlite')
c = conn.cursor()

if (len(sys.argv) != 2):
    quit ('Please provide card id')

card_number = str (sys.argv [1]);

#TODO: Check ID Valid Format
page = urllib2.urlopen('http://www.koolkingdom.co.uk/acatalog/info_' + card_number + '.html').read();
#TODO: Check not 404
#TOOD: Try again replace _ with -
#TODO: Try again add _1 to card_number
#TODO: Report Error
soup = BeautifulSoup(page)
soup.prettify()

#TODO: Clean price
card_name = soup.title.string

price = soup.find('actinic:prices').span
print price;
regex = re.compile(".*\xa3([0-9]+\.[0-9]+).*")
r = regex.search(str (price))
price = r.groups ()[0];

print card_number + " " + card_name + " " + price;

try:
    c.execute ("INSERT INTO cards VALUES (?, ?, ?, ?)", (card_number, card_name, 1, price))
    print "Added"
except sqlite3.IntegrityError as e:
    print "Duplicate"
    c.execute ("UPDATE cards SET qty = qty + 1, price = ? WHERE card_number = ?", (price, card_number));
    print "QTY Incremented and price updated"
conn.commit ()

c.close ();
