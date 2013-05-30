import urllib2
import sys
import re
import sqlite3

from BeautifulSoup import BeautifulSoup

conn = sqlite3.connect('cards.sqlite')
c = conn.cursor()

while True:
    card_number = raw_input("Card ID: ")
    card_number = card_number.upper();
    card_number = card_number.replace ("-", "_");

    if (card_number == ""):
        continue;
    elif card_number == "QUIT":
        break;

    url = 'http://www.koolkingdom.co.uk/acatalog/info_' + card_number + '.html';
    try:
        try:
            #Attempt to get page with standard URL
            page = urllib2.urlopen(url).read();
        except urllib2.HTTPError:
            #On failure attempt alternative
            page = urllib2.urlopen(url.replace ("_", "-")).read()
    except urllib2.HTTPError:
        print card_number + " could not be found"
        continue;

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
